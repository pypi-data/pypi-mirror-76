import requests
from bs4 import BeautifulSoup
from roulette_russe.Scraper import Scraper


class Choosemycompany(Scraper):
    def __init__(self, input_config, output_datasets, rr=None):
        super(Choosemycompany, self).__init__(input_config, output_datasets, rr)

    def get_pride(self, soup):
        return soup.findAll("a", {"id": "progress-fierte"})[0].findAll(
            "div", {"class": "progress-bar"})[0].attrs["aria-valuenow"]

    def get_company_logo_link(self, soup):
        if len(soup.findAll("a", {"class": "company-logo"})[0].findAll("img")) == 0:
            return ''
        return soup.findAll("a", {"class": "company-logo"})[0].findAll("img")[0].attrs['src']

    def get_professional_development(self, soup):
        return soup.findAll("a", {"id": "progress-developpement-professionnel"})[0].findAll("div", {
            "class": "progress-bar"})[0].attrs["aria-valuenow"]

    def get_motivation_and_management(self, soup):
        return soup.findAll("a", {"id": "progress-motivation-management"})[0].findAll("div", {"class": "progress-bar"})[
            0].attrs["aria-valuenow"]

    def get_fun_and_pleasure(self, soup):
        return soup.findAll("a", {"id": "progress-motivation-management"})[0].findAll("div", {"class": "progress-bar"})[
            0].attrs["aria-valuenow"]

    def get_employees_score(self, soup):
        return soup.findAll("a", {"class": "companypage-menu-section notation-block employees selected"})[0].findAll(
            "span", {"class": "notation rating"})[0].findAll("span")[0].text.replace('/ 5', '')

    def get_employees_raitings_count(self, soup):
        return \
            soup.findAll("div", {"class": "notation-legend text-right"})[0].text.replace(' ', '').replace('\n',
                                                                                                          '').split(
                'avis')[0].replace('\xa0', '0')

    def get_trainees_score(self, soup):
        return soup.findAll("a", {"class": "companypage-menu-section notation-block trainees"})[0].findAll("span", {
            "class": "notation rating"})[0].text.replace('/ 5', '')

    def get_trainees_raitings_count(self, soup):
        return \
            soup.findAll("div", {"class": "notation-legend text-right"})[1].text.replace(' ', '').replace('\n',
                                                                                                          '').split(
                'avis')[0].replace('\xa0', '0')

    def get_candidates_score(self, soup):
        return soup.findAll("a", {"class": "companypage-menu-section notation-block candidates"})[0].findAll("span", {
            "class": "notation rating"})[0].text.replace('/ 5', '')

    def get_candidates_raitings_count(self, soup):
        return \
            soup.findAll("div", {"class": "notation-legend text-right"})[2].text.replace(' ', '').replace('\n',
                                                                                                          '').split(
                'avis')[0].replace('\xa0', '0')

    def get_clients_score(self, soup):
        return soup.findAll("a", {"class": "companypage-menu-section notation-block clients"})[0].findAll("span", {
            "class": "notation rating"})[0].text.replace('/ 5', '')

    def get_clients_raitings_count(self, soup):
        return \
            soup.findAll("div", {"class": "notation-legend text-right"})[3].text.replace(' ', '').replace('\n',
                                                                                                          '').split(
                'avis')[0].replace('\xa0', '0')

    def get_simulating_env_rating(self, soup):
        return soup.findAll("a", {"id": "progress-environnement-de-travail"})[0].findAll(
            "div", {"class": "progress-bar"})[0].attrs["aria-valuenow"]

    def get_recognition_and_rewards_raiting(self, soup):
        return soup.findAll("a", {"id": "progress-salaire-reconnaissance"})[0].findAll(
            "div", {"class": "progress-bar"})[0].attrs["aria-valuenow"]

    def get_description(self, soup):
        return soup.findAll('div', {'class': 'activities-content'})[0].text

    def scrape_one_company(self, link):
        r = requests.get(link, proxies=self.get_proxies()).text
        soup = BeautifulSoup(r, 'html.parser')
        r = requests.get(link.replace('/salaries', '/infos'), proxies=self.get_proxies()).text
        soup_infos = BeautifulSoup(r, 'html.parser')
        return {
            'company_name': soup.findAll("h1")[0].text,
            'description': self.get_description(soup_infos),
            'company_logo': self.get_company_logo_link(soup),
            'global_score': soup.findAll("span", {"class": "average"})[0].text,
            'ratings_count': soup.findAll("span", {"class": "count"})[0].text,
            'employees_score': self.get_employees_score(soup),
            'employees_raitings_count': self.get_employees_raitings_count(soup),
            'trainees_score': self.get_trainees_score(soup),
            'trainees_raitings_count': self.get_trainees_raitings_count(soup),
            'candidates_score': self.get_candidates_score(soup),
            'candidates_raitings_count': self.get_candidates_raitings_count(soup),
            'clients_score': self.get_clients_score(soup),
            'clients_raitings_count': self.get_clients_raitings_count(soup),
            'stimulating_environment': self.get_simulating_env_rating(soup),
            'recognition_and_rewards': self.get_recognition_and_rewards_raiting(soup),
            'pride': self.get_pride(soup),
            'professional_development': self.get_professional_development(soup),
            'motivation_and_management': self.get_motivation_and_management(soup),
            'fun_and_pleasure': self.get_fun_and_pleasure(soup),
        }

    def scrap(self):
        tmp_list = []
        for link in self.input_config['links']:
            tmp_list.append(self.scrape_one_company(link))
        self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list, ignore_index=True)
        print(self.output_datasets['profiles'].head())

    def quality_check(self):
        pass
