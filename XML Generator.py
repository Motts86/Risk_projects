import xml.etree.ElementTree as ET
import csv
from datetime import datetime

board_csv = 'board.csv'
territories_csv = 'territories.csv'
continents_csv = 'continents.csv'
borders_csv = 'borders.csv'
cards_csv = 'cards.csv'
rules_csv = 'rules.csv'
colors_csv = 'colors.csv'

# Create a single root element
root = ET.Element('WarGearXML')

# Process board CSV
with open(board_csv, 'r') as csvfile:
    board_element = ET.SubElement(root, 'board')
    board_reader = csv.DictReader(csvfile)
    for row in board_reader:
        # Add the attributes directly to the board_element
        for key, value in row.items():
            board_element.set(key, value)

# Process territories CSV
with open(territories_csv, 'r') as csvfile:
    territories_element = ET.SubElement(root, 'territories')
    territories_reader = csv.DictReader(csvfile)
    for row in territories_reader:
        # Create a new element for each row
        element = ET.SubElement(territories_element, 'territory')

        # Add the attributes to the element
        for key, value in row.items():
            element.set(key, value)

# Process continents CSV
with open(continents_csv, 'r') as csvfile:
    continents_element = ET.SubElement(root, 'continents')
    continents_reader = csv.DictReader(csvfile)
    for row in continents_reader:
        # Create a new element for each row
        element = ET.SubElement(continents_element, 'continent')

        # Add the attributes to the element
        for key, value in row.items():
            element.set(key, value)

# Process borders CSV
with open(borders_csv, 'r') as csvfile:
    borders_element = ET.SubElement(root, 'borders')
    borders_reader = csv.DictReader(csvfile)
    for row in borders_reader:
        # Create a new element for each row
        element = ET.SubElement(borders_element, 'border')

        # Add the attributes to the element
        for key, value in row.items():
            element.set(key, value)

# Process cards CSV
with open(cards_csv, 'r') as csvfile:
    cards_element = ET.SubElement(root, 'cards')
    cards_reader = csv.DictReader(csvfile)
    for row in cards_reader:
        # Add the attributes to the cards element
        card_element = ET.SubElement(cards_element, 'card')
        for key, value in row.items():
            card_element.set(key, value)

# Process rules CSV
with open(rules_csv, 'r') as csvfile:
    rule_element = ET.SubElement(root, 'rules')
    rules_reader = csv.DictReader(csvfile)
    for row in rules_reader:
        # Add the attributes directly to the board_element
        for key, value in row.items():
            rule_element.set(key, value)

# Process colors CSV
with open(colors_csv, 'r') as csvfile:
    colors_element = ET.SubElement(root, 'colors')
    colors_reader = csv.DictReader(csvfile)
    for row in colors_reader:
        # Create a new element for each row
        element = ET.SubElement(colors_element, 'color')

        # Add the attributes to the element
        for key, value in row.items():
            element.set(key, value)

date = datetime.now().date()

# Write the final XML tree to a file
tree = ET.ElementTree(root)
tree.write(f'Import_XML_{date}.xml')