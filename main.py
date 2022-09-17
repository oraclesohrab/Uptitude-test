import pandas as pd
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


class WebsiteDetails:
    def __init__(self, website):
        try:
            self.content = website.content
            self.url = website.url
            self.links = self._GetWebSiteLinks()
            self.data = [['status_code',
                          'encoding',
                          'elapsed',
                          'Content-Type',
                          'internal_links',
                          'external_links'],
                         [website.status_code,
                          website.encoding,
                          website.elapsed,
                          website.headers['Content-Type'],
                          self.links.get('internal', None),
                          self.links.get('external', None)
                          ]
                         ]
            self._print_data_frame()
        except Exception as e:
            raise e

    def _print_data_frame(self):
        df = pd.DataFrame(self.data[1:], columns=self.data[0])
        print(df)

    def _GetWebSiteLinks(self):
        """
        Returns all URLs that is found on `url` in which it belongs to the same website
        """
        # all URLs of `url`
        urls = dict()
        internal_urls = list()
        external_urls = list()
        # domain name of the URL without the protocol
        domain_name = urlparse(self.url).netloc
        soup = BeautifulSoup(self.content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                if href not in external_urls:
                    external_urls.append(href)
                continue
            internal_urls.append(href)
            urls['internal'] = internal_urls
            urls['external'] = external_urls
        return urls


def is_valid(web_url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(web_url)
    return bool(parsed.netloc) and bool(parsed.scheme)


if __name__ == '__main__':
    url = input("Please Enter the Website URL (e.g., https://www.imdb.com): ")
    while True:
        if not is_valid(url):
            url = input("URL is not valid. Please enter a valid URL (e.g., https://www.imdb.com): ")
        else:
            try:
                response = requests.get(url)
                break
            except ConnectionError:
                url = input("URL not found. Please enter a correct URL (e.g., https://www.imdb.com): ")

    WebsiteDetails(response)
    response.close()
