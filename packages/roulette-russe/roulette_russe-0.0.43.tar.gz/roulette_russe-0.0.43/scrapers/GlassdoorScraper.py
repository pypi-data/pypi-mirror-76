import requests
from bs4 import BeautifulSoup
from roulette_russe.Scraper import Scraper


class GlassdoorScraper(Scraper):
    def __init__(self, input_config, output_datasets, rr=None):
        super(GlassdoorScraper, self).__init__(input_config, output_datasets, rr)

    def get_company_logo(self, soup):
        return soup.findAll("span",{"class": "sqLogo"})[0].findAll("img")[0].attrs['src']

    def get_company_name(self, soup):
        return soup.findAll("span",{"id": "DivisionsDropdownComponent"})[0].text

    def get_company_description(self, soup):
        return soup.findAll("div", {"class": "empDescription"})[0].text

    def get_number_of_reviews(self, soup):
        return soup.findAll("a", {"class":"reviews"})[0].findAll("span", {"class": "num"})[0].text

    def get_number_of_jobs(self, soup):
        return soup.findAll("a", {"class":"jobs"})[0].findAll("span", {"class": "num"})[0].text

    def get_number_of_salaries(self, soup):
        return soup.findAll("a", {"class":"salaries"})[0].findAll("span", {"class": "num"})[0].text

    def get_number_of_interviews(self, soup):
        return soup.findAll("a", {"class":"interviews"})[0].findAll("span", {"class": "num"})[0].text

    def get_number_of_benefits(self, soup):
        return soup.findAll("a", {"class":"benefits"})[0].findAll("span", {"class": "num"})[0].text

    def get_number_of_photos(self, soup):
        return soup.findAll("a", {"class":"photos"})[0].findAll("span", {"class": "num"})[0].text

    def get_overall_rating(self, text):
        return text.split('overallRating":')[1].split(',')[0]

    def get_ceoRating(self, text):
        return text.split('ceoRating":')[1].split(',')[0]

    def get_ceoRating_count(self, text):
        return text.split('ceoRatingsCount":')[1].split(',')[0]

    def get_career_opportunities_rating(self, text):
        return text.split('careerOpportunitiesRating":')[1].split(',')[0]

    def get_work_life_balance(self, text):
        return text.split('workLifeBalanceRating":')[1].split(',')[0]

    def get_business_outlook_rating(self, text):
        return text.split('businessOutlookRating":')[1].split(',')[0]

    def get_senior_management_rating(self, text):
        return text.split('seniorManagementRating":')[1].split(',')[0]

    def get_compensation_and_benefits_rating(self, text):
        return text.split('compensationAndBenefitsRating":')[1].split(',')[0]

    def get_culture_and_values_rating(self, text):
        return text.split('cultureAndValuesRating":')[1].split(',')[0]

    def scrape_profile(self, link):
        r = requests.get(link, headers={
            'User-Agent': self.get_laptop_user_agent()
        }, proxies=self.get_proxies()).text

        soup = BeautifulSoup(r, 'html.parser')
        reviews_link = "https://www.glassdoor.fr" + soup.findAll("a", {"class": "reviews"})[0].attrs['href']
        r_reviews = requests.get(reviews_link, headers={
            'User-Agent': self.get_laptop_user_agent()
        }, proxies=self.get_proxies()).text
        return {
            "company_name": self.get_company_name(soup),
            "company_logo": self.get_company_logo(soup),
            "number_of_reviews": self.get_number_of_reviews(soup),
            "number_of_jobs": self.get_number_of_jobs(soup),
            "number_of_salaries": self.get_number_of_salaries(soup),
            "number_of_interviews": self.get_number_of_interviews(soup),
            "number_of_benefits": self.get_number_of_benefits(soup),
            "number_of_photos": self.get_number_of_photos(soup),
            "overall_rating": self.get_overall_rating(r_reviews),
            "ceo_rating": self.get_ceoRating(r_reviews),
            "ceo_rating_count": self.get_ceoRating_count(r_reviews),
            "career_opportunities_rating": self.get_career_opportunities_rating(r_reviews),
            "work_life_balance_rating": self.get_work_life_balance(r_reviews),
            "business_outlook_rating": self.get_business_outlook_rating(r_reviews),
            "senior_management_rating": self.get_senior_management_rating(r_reviews),
            "compensation_and_benefits_rating": self.get_compensation_and_benefits_rating(r_reviews),
            "culture_and_values_rating": self.get_culture_and_values_rating(r_reviews)
        }

    def scrap(self):
        tmp_list = []
        if 'profiles' in self.output_datasets:
            for link in self.input_config['links']:
                profile_data = self.scrape_profile(link)
                tmp_list.append(profile_data)
            self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list, ignore_index=True)

    def quality_check(self):
        pass