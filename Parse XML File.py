import xml.etree.ElementTree as ET
import pandas as pd
import os

MapFileXML = 'Peak Knowledge.xml'
tree = ET.parse(MapFileXML)
root = tree.getroot()

# Get Board Element
board_element = root.find('.//board')
data_board = {attribute: board_element.attrib[attribute] for attribute in board_element.attrib}
df_board = pd.DataFrame([data_board])

rules_element = root.find('.//rules')
data_rules = {attribute: rules_element.attrib[attribute] for attribute in rules_element.attrib}
df_rules = pd.DataFrame([data_rules])

# Get Territory Elements from Territories
data_territories = []
territories_element = root.find('.//territories')
if territories_element is not None:
    for territory_element in territories_element.findall('.//territory'):
        territory_data = {attribute: territory_element.attrib[attribute] for attribute in territory_element.attrib}
        data_territories.append(territory_data)
df_territories = pd.DataFrame(data_territories)

# Get Continent Elements from Continents
data_continents = []
continents_element = root.find('.//continents')
if continents_element is not None:
    for continent_element in continents_element.findall('.//continent'):
        continent_data = {attribute: continent_element.attrib[attribute] for attribute in continent_element.attrib}
        data_continents.append(continent_data)
df_continents = pd.DataFrame(data_continents)

# Get Border Elements from Borders
data_borders = []
borders_element = root.find('.//borders')
if borders_element is not None:
    for border_element in borders_element.findall('.//border'):
        border_data = {attribute: border_element.attrib[attribute] for attribute in border_element.attrib}
        data_borders.append(border_data)
df_borders = pd.DataFrame(data_borders)

# Get Card Elements from Cards
data_cards = []
cards_element = root.find('.//cards')
if cards_element is not None:
    for card_element in cards_element.findall('.//card'):
        card_data = {attribute: card_element.attrib[attribute] for attribute in card_element.attrib}
        data_cards.append(card_data)
df_cards = pd.DataFrame(data_cards)

# Get Color Elements from Colors
data_colors = []
colors_element = root.find('.//colors')
if colors_element is not None:
    for color_element in colors_element.findall('.//color'):
        color_data = {attribute: color_element.attrib[attribute] for attribute in color_element.attrib}
        data_colors.append(color_data)
df_colors = pd.DataFrame(data_colors)

# Output XML files to CSV
script_dir = os.path.dirname(os.path.realpath(__file__))

board_output_file_name = "board.csv"
board_output_fp = os.path.join(script_dir, board_output_file_name)
df_board.to_csv(board_output_fp, index=False)

continent_output_file_name = "continents.csv"
continent_output_fp = os.path.join(script_dir, continent_output_file_name)
df_continents.to_csv(continent_output_fp, index=False)

territories_output_file_name = "territories.csv"
territory_output_fp = os.path.join(script_dir, territories_output_file_name)
df_territories.to_csv(territory_output_fp, index=False)

borders_output_file_name = "borders.csv"
border_output_fp = os.path.join(script_dir, borders_output_file_name)
df_borders.to_csv(border_output_fp, index=False)

cards_output_file_name = "cards.csv"
card_output_fp = os.path.join(script_dir, cards_output_file_name)
df_cards.to_csv(card_output_fp, index=False)

colors_output_file_name = "colors.csv"
color_output_fp = os.path.join(script_dir, colors_output_file_name)
df_colors.to_csv(color_output_fp, index=False)

rules_output_file_name = "rules.csv"
rules_output_fp = os.path.join(script_dir, rules_output_file_name)
df_rules.to_csv(rules_output_fp, index=False)


