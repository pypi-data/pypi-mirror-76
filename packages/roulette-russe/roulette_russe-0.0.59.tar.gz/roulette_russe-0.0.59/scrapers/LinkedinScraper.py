from roulette_russe.Scraper import Scraper

class LinkedinScraper(Scraper):
    def __init__(self, input_config, output_datasets, username, password, rr=None):
        super(LinkedinScraper, self).__init__(input_config, output_datasets, rr)

    def scrap(self):
        pass

    def quality_check(self):
        pass
