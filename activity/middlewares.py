from scrapy import Spider
from scrapy.crawler import Crawler


class ActivitySpiderMiddleware:
    """
    Spider middleware for intercepting and processing responses, exceptions,
    and initial requests during a spider's execution.
    """


    @classmethod
    def from_crawler(cls) -> 'ActivitySpiderMiddleware':
        """
        Initializes the middleware. You can add signal connections here if needed.

        Args:
            crawler (Crawler): The Scrapy crawler instance.

        Returns:
            ActivitySpiderMiddleware: An instance of the middleware.
        """
        return cls()


class ActivityDownloaderMiddleware:
    """
    Downloader middleware for handling requests and responses during
    the downloading process.
    """


    @classmethod
    def from_crawler(cls) -> 'ActivityDownloaderMiddleware':
        """
        Initializes the middleware.

        Args:
            crawler (Crawler): The Scrapy crawler instance.

        Returns:
            ActivityDownloaderMiddleware: An instance of the middleware.
        """
        return cls()
