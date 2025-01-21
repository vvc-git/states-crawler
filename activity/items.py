import scrapy


class City(scrapy.Item):
    """
    Represents a city with its attributes to be scraped.

    Fields:
        - name: The name of the city (e.g., "Adamantina").
        - state: The state where the city is located (e.g., "São Paulo").
        - distance_to_the_capital: The distance to the capital city of the state (e.g., "56 km").
        - total_population: The total population as a string (e.g., "35 068 hab.").
        - total_area: The total area of the city (e.g., "411,781 km²").
        - density: The population density per square kilometer (e.g., "81,37hab./km²").
        - hdi: The Human Development Index (e.g., "0,790").
        - url: Source URL where the city's information is scraped from.
    """
    name = scrapy.Field()
    state = scrapy.Field()
    distance_to_the_capital = scrapy.Field()
    total_population = scrapy.Field()
    total_area = scrapy.Field()
    density = scrapy.Field()
    hdi = scrapy.Field()
    url = scrapy.Field()
