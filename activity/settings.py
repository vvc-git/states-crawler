# The name of the Scrapy project. This is used internally by Scrapy to identify the project.
BOT_NAME = 'activity'

# The modules where Scrapy will look for spiders.
# This is the main location for the custom spiders.
SPIDER_MODULES = ['activity.spiders']

# The module where Scrapy will create new spiders when you use the `genspider` command.
NEWSPIDER_MODULE = 'activity.spiders'

# Follow the rules defined in the website's robots.txt file to ensure ethical scraping.
ROBOTSTXT_OBEY = True

# Configure pipelines to process and export the scraped data.
# Each pipeline is assigned a priority number, where lower numbers execute first.
ITEM_PIPELINES = {
    'activity.pipelines.JsonWriterPipeline': 400,  # Saves data to a JSON file.
    'activity.pipelines.CSVWriterPipeline': 400,  # Saves data to a CSV file.
}
