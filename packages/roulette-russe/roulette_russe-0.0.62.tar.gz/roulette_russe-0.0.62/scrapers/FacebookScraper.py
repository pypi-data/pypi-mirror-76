from roulette_russe.Scraper import Scraper
from facebook_scraper import get_posts
import requests
from bs4 import BeautifulSoup

class FacebookScraper(Scraper):
    def __init__(self, input_config, output_datasets, rr=None):
        super(FacebookScraper, self).__init__(input_config, output_datasets, rr)

    def query_posts(self, account):
        return get_posts(account=account,page_limit=20, options=[])

    def query_company_infos(self, account):
        r = requests.get('https://m.facebook.com/'+account+'/?locale2=fr_FR', headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'
        }, proxies=self.get_proxies()).text

        # Extract main infos
        soup = BeautifulSoup(r, 'html.parser')

        # Extract account name
        name = soup.findAll('div', {"id": 'u_0_d'})[0].text

        # Extract logo
        logo = soup.findAll('img', {"id": "u_0_5"})[0]['src']
        # Extract community
        r2 = requests.get('https://m.facebook.com/'+account+'/community/', headers={
            'User-Agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
        }, proxies=self.get_proxies()).text
        soup2 = BeautifulSoup(r2, 'html.parser')
        number_of_likes = soup2.findAll('div', {"class": "bn"})[0].text
        number_of_followers = soup2.findAll('div', {"class": "bn"})[1].text

        return {
            'name': name,
            'logo': logo,
            'number_of_likes': number_of_likes,
            'number_of_followers': number_of_followers
        }

    def scrap(self):
        tmp_list_profiles = []
        tmp_list_posts = []
        for account in self.input_config['accounts']:
            profile_data = self.query_company_infos(account)
            tmp_list_profiles.append(profile_data)
        self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list_profiles, ignore_index=True)
        if 'posts' in self.output_datasets:
            for account in self.input_config['accounts']:
                self.output_datasets['posts'] = self.output_datasets['posts'].append(
                    list(self.query_posts(account)),
                    ignore_index=True)
        pass

    def quality_check(self):
        pass
