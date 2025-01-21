import scrapy
from activity.items import City


class CitiesSpider(scrapy.Spider):
    """
    Spider to scrape city data from Wikipedia.
    Navigates through a list of municipalities and extracts details like name, state, total_population, total area, HDI and source url.
    """
    name = 'cities'  # Unique name for this spider
    allowed_domains: list[str] = ['pt.wikipedia.org']  # Allowed domains for scraping
    BASE_URL: str = 'https://pt.wikipedia.org'  # Base URL for constructing full links
    
    # List of starting URLs containing municipality data
    start_urls: list[str] = [
        'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_S%C3%A3o_Paulo',
        'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_de_Janeiro',
        'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Minas_Gerais'
    ]

    def parse(self, response: scrapy.http.Response) -> scrapy.Request:
        """
        Parses the main list pages of municipalities and extracts links to individual city pages.

        Args:
            response (scrapy.http.Response): HTTP response from the starting URL.

        Yields:
            scrapy.Request: Requests for individual city pages with metadata.
        """
        # Select all city links from the table
        city_links = response.xpath('//td[position() = 2]/a')
        
        for city in city_links:
            name: str = city.xpath('./text()').get()  # Get the city's name
            href: str = city.xpath('./@href').get()  # Get the relative URL to the city's page
            
            if name and href:  # Ensure both name and link exist
                # Schedule a request for the city's details page
                yield scrapy.Request(
                    url=f"{self.BASE_URL}{href}",
                    callback=self.parse_city,
                    meta={'city_name': name}
                )

    def parse_city(self, response: scrapy.http.Response) -> City:
        """
        Parses an individual city's page to extract detailed information.

        Args:
            response (scrapy.http.Response): HTTP response from the city's page.

        Yields:
            City: The City object containing extracted data.
        """
        city_name: str = response.meta.get('city_name')  # Retrieve city name from metadata
        infobox = response.xpath('//table[contains(@class, "infobox")]')  # Locate the infobox table

        # Extract city details
        city = City(
            name=city_name,
            state=self.extract_text(infobox, './/tr[.//*[contains(text(), "Unidade federativa")]]/td[2]/a/text()'),
            distance_to_the_capital=self.extract_text(infobox, './/tr[.//*[contains(text(), "Distância até a")]]/td[2]/text()'),
            total_population=self.extract_text(infobox, './/tr[.//*[contains(text(), "Popula")]]/td[2]/text()'),
            total_area=self.extract_text(infobox, './/tr[.//*[contains(text(), "rea total")]]/td[2]/text()'),
            density=self.extract_text(infobox, './/tr[.//*[contains(text(), "ensidade")]]/td[2]/span/text()'),
            hdi=self.extract_text(infobox, './/tr[.//*[contains(text(), "IDH")]]/td[2]/text()'),
            url=response.url  # Include the URL of the page for reference
        )

        yield city

    def extract_text(self, selector: scrapy.selector.Selector, xpath: str) -> str:
        """
        Extracts and cleans text from an XPath query.

        Args:
            selector (scrapy.selector.Selector): The selector to query.
            xpath (str): The XPath query.

        Returns:
            str: The cleaned text or an empty string if no text is found.
        """
        text: str = selector.xpath(xpath).get(default='')  # Extract text or return an empty string
        return text.strip().replace('\xa0', '').replace('\n', '')  # Clean up unwanted characters
