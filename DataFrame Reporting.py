from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from collections import Counter, defaultdict


def get_elements(driver: webdriver, locator: tuple[str, str], wait_time: int = 10, many: bool = False):
    """
    Waits for the presence of elements based on the given locator.

    Args:
        driver (WebDriver): The Chrome WebDriver instance.
        locator (tuple): A tuple (By, str) representing the locator strategy and value.
        wait_time (int, optional): The maximum time to wait for the elements. Default is 10 seconds.
        many (bool, optional): If True, waits for the presence of all elements; if False, waits for a single element.

    Returns:
        list or WebElement: A list of elements if 'many' is True, otherwise a single WebElement.
        Returns None if the elements are not found within the specified wait time.
    """
    if many:
        try:
            elements = WebDriverWait(driver, wait_time).until(
                ec.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            print(f"TimeoutException: Timed out waiting for elements with locator: {locator}")
            return None
    else:
        try:
            elements = WebDriverWait(driver, wait_time).until(
                ec.presence_of_element_located(locator)
            )
            return elements
        except TimeoutException:
            print(f"TimeoutException: Timed out waiting for elements with locator: {locator}")
            return None


def open_pop_up_by_xpath(driver: webdriver, xpath):
    """
    Clicks on an element identified by XPath to open a pop-up.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        xpath (str): XPath of the element to be clicked.
    """
    trigger_element = get_elements(driver, (By.XPATH, xpath))
    trigger_element.click()


def extract_player_colors(driver: webdriver) -> Dict[str, str]:
    """
    Extracts player colors and returns a dictionary mapping player names to color values.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.

    Returns:
        Dict[str, str]: A dictionary mapping player names to color values.
    """
    player_color: Dict[str, str] = {}

    # XPath to locate player color <tr> elements
    player_color_xpath = '//*[@id="bs_infobar"]/table/tbody/tr[position() > 1]'

    # Explicitly wait for the presence of player color <tr> elements
    player_color_elements: List[WebElement] = (
        get_elements(driver, (By.XPATH, player_color_xpath), 10, True))

    for player_color_element in player_color_elements:
        try:
            # Extract values from <td> and <a> elements
            td_element: WebElement = player_color_element.find_element(By.XPATH, './td[3]')
            a_element: WebElement = td_element.find_element(By.TAG_NAME, 'a')

            # Use JavaScript to get the raw style attribute value
            style_attribute: str = driver.execute_script("return arguments[0].getAttribute('style');", td_element)
            a_text: str = a_element.text

            # Strip unwanted parts from the style attribute
            color_value: str = style_attribute.replace("background-color:", "").strip()

            # Update the dictionary with the relationship between text of <a> and style attribute
            player_color[a_text] = color_value
        except Exception as e:
            # Handle exceptions (print or log the error)
            print(f"Error extracting player color: {e}")
    return player_color


def main(website):
    driver = webdriver.Chrome()
    # Open website
    driver.get(website)

    try:
        # This will open relevant pop-up widgets
        open_pop_up_by_xpath(driver, '/ html / body / div / div[8] / table / tbody / tr[1] / td / span[3] / a[6]')
        open_pop_up_by_xpath(driver, '/html/body/div/div[8]/table/tbody/tr[1]/td/span[3]/a[5]')

        # Configure Dictionaries
        fill_value_records, results = {}, {}
        player_color = extract_player_colors(driver)
        bonus_dict = defaultdict(int)

        # Capture Rules Elements
        gamename = get_elements(driver, (By.XPATH, '//*[@id="breadcrumbs"]/a[3]')).text
        n = int(
            get_elements(driver, (By.XPATH, '//*[@id="boardabout"]/table[4]/tbody/tr[1]/td[1]/b')).text.strip(
                " ")[0])
        n_troops_per_territory = int(
            get_elements(driver, (By.XPATH, '//*[@id="boardabout"]/table[4]/tbody/tr[1]/td[2]/b')).text)
        min_troops = int(
            get_elements(driver, (By.XPATH, '//*[@id="boardabout"]/table[4]/tbody/tr[2]/td[2]/b')).text)

        # Extract the fill values for all territories
        territory_fill_elements = (
            get_elements(driver, (By.CSS_SELECTOR, 'div#bs_canvas_fillmap svg path'), 10, True))

        # Record fill color counts inside fill_value_records dict
        fill_value = [element.get_attribute('fill') for element in territory_fill_elements]
        fill_value_records = Counter(fill_value)

        # Lookup continent bonuses
        tr_elements = get_elements(driver, (By.CSS_SELECTOR, 'table#bs_continent_table tbody')).find_elements(
            By.TAG_NAME, 'tr')

        # Fill dictionary with bonuses
        for tr_element in tr_elements:
            username = tr_element.find_element(By.CLASS_NAME, 'bs_continent_table_col3').text
            try:
                bs_plus_element = tr_element.find_element(By.CSS_SELECTOR, '.bs_continent_table_col2 .bs_plus')
                bonus = int(bs_plus_element.text)
            except NoSuchElementException:
                try:
                    bs_minus_element = tr_element.find_element(By.CSS_SELECTOR, '.bs_continent_table_col2 .bs_minus')
                    bonus = int(bs_minus_element.text)
                except NoSuchElementException:
                    bonus = 0  # Handle the case when neither .bs_plus nor .bs_minus is present
            bonus_dict[username] += bonus

    except Exception as e:
        print(f"Error: {e}")

    # Close the browser window
    finally:
        driver.quit()

    # Creates dictionary with color as key, username as data
    color_player = {color: username for username, color in player_color.items()}

    for fill_value, count in fill_value_records.items():
        if fill_value != '#aaaaaa':
            # maps report attributes
            if count // n_troops_per_territory < min_troops:
                troops_from_territory = min_troops
            else:
                troops_from_territory = (count // n_troops_per_territory) * n
            if color_player[fill_value] in bonus_dict:
                bonus = bonus_dict[color_player[fill_value]]
            else:
                bonus = 0
            player = color_player[fill_value]

            # Populate Results in Dictionary
            results[player] = {
                'territories': count,
                'terr troops': troops_from_territory,
                'rmdrs': count % n_troops_per_territory,
                'bonus troops': bonus,
                'reserves': bonus + troops_from_territory
            }
        else:
            results["Neutral"] = {
                'territories': count,
                'terr troops': 0,
                'rmdrs': 0,
                'bonus troops': 0,
                'reserves': 0
            }
    df = pd.DataFrame.from_dict(results, orient='index').sort_values('reserves', ascending=False)

    # Print the Results
    print(f"""

Game Name : {gamename}
URL       : {website}

    * "{n}" Troop(s) Per "{n_troops_per_territory}" Territories
    * Min Troops: {min_troops}

Results:
    {df}""")


if __name__ == "__main__":
    main("https://www.wargear.net/games/player/81406920")
