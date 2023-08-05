from typing import List
import os
from urllib.request import Request, urlopen

import bs4
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time
import pandas as pd
from getnews.Logging_skelton import Config
import socket


class RssScrapper(Config):
    def __init__(self):
        Config.__init__(self)
        self.file = None
        self.News = []
        self.rss_info = dict()
        self.soup = None
        self.success_logger = self.create_success_logger()
        self.failure_logger = self.create_failure_logger()

    def read_data(self, file) -> list:
        self.file = file
        try:
            f1 = open(self.file, 'r')
            lines: List[str] = f1.readlines()
            assert type(lines) == list, "Something wrong in reading"
            assert len(lines) != 0, "The file is empty nothing to read"
            self.success_logger.info("File read Successfully")
            return lines
        except AssertionError as e:
            self.failure_logger.exception(e)
        except Exception as e:
            self.failure_logger.exception(e)

    def create_soup(self, url):
        try:
            container = Request(url, headers={'User-Agent': 'Chrome/83.0.4103.116'})
            website = urlopen(container, timeout=50).read()
            self.soup: BeautifulSoup = BeautifulSoup(website, 'xml')
            return self.soup

        except HTTPError as err:
            if err.code == 404:
                self.failure_logger.info("{} ----> Url doesn't exist".format(url))
                return err.code

            if err.code == 400:
                self.failure_logger.info('URL {}: ----> 400 Bad Request error'.format(url))
                return err.code

        except TimeoutError as te:
            self.failure_logger.info('URL {}: ----> Timeout error'.format(url))
            return te

        except (socket.timeout, socket.gaierror) as err:
            self.failure_logger.info('URL {}: ----> socket timeout error'.format(url))
            return err

        except Exception as e:
            self.failure_logger.info('URL {}:----> Some other error'.format(url))
            self.failure_logger.exception(e)
            return e

    def items(self, soup):
        self.soup = soup
        try:
            if self.soup.findAll('item'):
                news_data = self.soup.findAll('item')
                return news_data
            elif self.soup.findAll('entry'):
                news_data = self.soup.findAll('entry')
                return news_data
            else:
                news_data = []
                return news_data
        except Exception as e:
            self.failure_logger.exception(e)

    def get_data(self, data, source):
        try:
            for i in data:
                self.rss_info = dict()
                # Titles
                try:
                    self.rss_info['Title'] = i.title.text
                except Exception:
                    self.rss_info['Title'] = None

                    # URL's
                try:
                    if i.find('link', {'rel': 'alternate'}):
                        self.rss_info['Url'] = i.link['href']
                    elif i.link:
                        self.rss_info['Url'] = i.link.text
                except Exception:
                    self.rss_info['Url'] = None

                # Descriptions
                try:
                    if i.description:
                        self.rss_info['Description'] = i.description.text
                    elif i.find('content', {'type': 'html'}):
                        self.rss_info['Description'] = i.find('content', {'type': 'html'}).text
                    elif i.find('content:encoded'):
                        self.rss_info['Description'] = i.find('content:encoded').text
                except Exception:
                    self.rss_info['Description'] = None

                # Date
                try:
                    if i.pubDate:
                        self.rss_info['Date'] = i.pubDate.text
                    elif i.published:
                        self.rss_info['Date'] = i.published.text
                except Exception:
                    self.rss_info['Date'] = None

                try:
                    self.rss_info["Source"] = source
                except Exception:
                    self.rss_info["Source"] = None
                self.News.append(self.rss_info)
                del self.rss_info
            self.success_logger.info("{} ----> Completed".format(source)+" (Found {} news)".format(len(data)))

        except Exception as e:
            self.failure_logger.info("{} ----> error while getting the info".format(source))
            self.failure_logger.exception(e)

    def get_all(self, file):
        try:
            empty = type(None)
            assert type(file) is str, "The name of the file should be in String only"
            assert os.path.exists(file), "The text file is not there in the directory"
            lines = self.read_data(file=file)
            assert type(lines) is not empty, "The text file return nothing"
            for line in lines:
                line = line.strip()
                time.sleep(2)
                self.success_logger.info("{} ----> Started".format(line))
                soup = self.create_soup(line)
                if type(soup) is bs4.BeautifulSoup:
                    news_data = self.items(soup)
                    if len(news_data) != 0:
                        self.get_data(news_data, line)
                    else:
                        self.success_logger.info("{} ----> No news available".format(line))
                        continue
                else:
                    continue
            try:
                full_news = pd.DataFrame(self.News)
                full_news.to_csv("Final_news.csv", index=False)
                self.success_logger.info("File has been successfully Saved")
            except Exception as e:
                self.failure_logger.info("Error while saving the file")
                self.failure_logger.exception(e)
        except AssertionError as e:
            self.failure_logger.exception(e)
        except Exception as e:
            self.failure_logger.exception(e)
