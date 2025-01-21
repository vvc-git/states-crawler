import os
import json
import csv
import unicodedata
from typing import Dict
from scrapy.item import Item
from scrapy.spiders import Spider


class ActivityPipeline:
    """
    A basic pipeline template that processes items without modifying them.
    """


    def process_item(self, item: Item, spider: Spider) -> Item:
        """
        Processes each item without modification.

        Args:
            item (Item): The scraped item.
            spider (Spider): The spider instance that scraped the item.

        Returns:
            Item: The unmodified item.
        """
        return item


class JsonWriterPipeline:
    """
    Pipeline to write scraped items to JSON files grouped by state.
    Each state's data is written into a separate JSON file.
    """


    def __init__(self) -> None:
        """
        Initializes the pipeline with placeholders for output directory and file handles.
        """
        self.output_dir: str = 'output_json'
        self.files: Dict[str, 'file'] = {}  # File handles for each state


    def open_spider(self, spider: Spider) -> None:
        """
        Ensures the output directory exists when the spider is opened.

        Args:
            spider (Spider): The spider instance that scraped the item.
        """
        os.makedirs(self.output_dir, exist_ok=True)


    def close_spider(self, spider: Spider) -> None:
        """
        Closes all open JSON files when the spider finishes.

        Args:
            spider (Spider): The spider instance that scraped the item.
        """
        for file in self.files.values():
            file.write('\n') # Add a newline
            file.write(']')  # Close the JSON array
            file.close()


    def process_item(self, item: Item, spider: Spider) -> Item:
        """
        Writes the item's data to the corresponding state's JSON file.

        Args:
            item (Item): The scraped item.
            spider (Spider): The spider instance that scraped the item.

        Returns:
            Item: The processed item.
        """
        state: str = unicodedata.normalize('NFKD', item['state']).encode('ASCII', 'ignore').decode('utf-8').lower().replace(' ', '_') # Normalize the state name
    
        # Check if the 'state' field is present and not empty
        if 'state' not in item or not item['state']:
            file_name: str = "error.json"
            file_path: str = os.path.join(self.output_dir, file_name)
        else:
            file_name: str = f"{state}.json"
            file_path: str = os.path.join(self.output_dir, file_name)

        # If the file is not already open, initialize it
        if state not in self.files:
            self.files[state] = open(file_path, 'w', encoding='utf-8')
            self.files[state].write('[\n')  # Start the JSON array with proper formatting

        # Write the current item as a JSON object
        file = self.files[state]
        file.seek(0, os.SEEK_END)  # Move the cursor to the end of the file
        if file.tell() > 2:  # If the file is not empty (more than just the opening '[')
                file.write(',\n')  # Add a comma and a newline before appending a new item
        
        # Dump the item with proper indentation
        json.dump(dict(item), file, ensure_ascii=False, indent=4)

        return item


class CSVWriterPipeline:
    """
    Pipeline to write scraped items to separate CSV files based on the state.
    Each state's data is written into a separate CSV file.
    """


    def __init__(self) -> None:
        """
        Initializes the pipeline with placeholders for output directory, file handles, and writers.
        """
        self.output_dir: str = 'output_csv'
        self.files: Dict[str, 'file'] = {}  # File handles for each state
        self.writers: Dict[str, csv.writer] = {}  # CSV writer objects for each state


    def open_spider(self, spider: Spider) -> None:
        """
        Ensures the output directory exists when the spider is opened.

        Args:
            spider (Spider): The spider instance that scraped the item.
        """
        os.makedirs(self.output_dir, exist_ok=True)


    def close_spider(self, spider: Spider) -> None:
        """
        Closes all open CSV files when the spider finishes.

        Args:
            spider (Spider): The spider instance that scraped the item.
        """
        for file in self.files.values():
            file.close()


    def process_item(self, item: Item, spider: Spider) -> Item:
        """
        Writes the item's data to the corresponding state's CSV file.

        Args:
            item (Item): The scraped item.
            spider (Spider): The spider instance that scraped the item.

        Returns:
            Item: The processed item.
        """
        state: str = unicodedata.normalize('NFKD', item['state']).encode('ASCII', 'ignore').decode('utf-8').lower().replace(' ', '_') # Normalize the state name
    
        # Check if the 'state' field is present and not empty
        if 'state' not in item or not item['state']:
            file_name: str = "error.csv"
            file_path: str = os.path.join(self.output_dir, file_name)
        else:
            file_name: str = f"{state}.csv"
            file_path: str = os.path.join(self.output_dir, file_name)

        # If the file is not already open, initialize it
        if state not in self.files:
            # Open the file and create a CSV writer
            self.files[state] = open(file_path, 'w', newline='', encoding='utf-8')
            self.writers[state] = csv.writer(self.files[state])
            # Write the header row
            self.writers[state].writerow(['Name', 'State', 'Distance to the Capital (Km)','Total Population', 'Total Area', 'Density', 'HDI', 'URL'])

        # Write the item as a row in the CSV file
        self.writers[state].writerow([
            item['name'], item['state'], item['distance_to_the_capital'],item['total_population'], item['total_area'], item['density'],item['hdi'], item['url']
        ])

        return item
