from getnews.main import RssScrapper

class ScrapNews:

    def Start_Scrapping(self):
        a = RssScrapper()
        a.get_all(file="C:/Users/rudra/Downloads/Inter_Project/getnews/Feed_URLs.txt")

