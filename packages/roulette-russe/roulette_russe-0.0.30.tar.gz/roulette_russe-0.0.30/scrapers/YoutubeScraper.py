import requests

from roulette_russe.Scraper import Scraper


class YoutubeScraper(Scraper):
    def __init__(self, input_config, output_datasets, rr=None):
        super(YoutubeScraper, self).__init__(input_config, output_datasets, rr)

    def extract_channel_title(self, payload):
        return payload['metadata']['channelMetadataRendered']['title']

    def extract_channel_description(self, payload):
        return payload['metadata']['channelMetadataRendered']['description']

    def extract_channel_keywords(self, payload):
        return payload['metadata']['channelMetadataRendered']['keywords'].split(' ')

    def extract_channel_logo(self, payload):
        return payload['metadata']['channelMetadataRendered']['avatar']['thumbnails'][0]['url']

    def extract_number_of_subscribers(self, payload):
        return payload['header']['c4TabbedHeaderRendere']['subscriberCountText']['runs'][0]['text'].split(' ')[0]

    def extract_number_of_views(self, payload):
        for tab in payload['contents']['twoColumnBrowseResultsRenderer']['tabs']:
            if tab['tabRenderer']['title'] == "À propos":
                return int(tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer'][
                               'contents'][0]['viewCountText']['runs'][0]['text'].replace(' ', ''))

    def scrape_channel_profile(self, channel_id):
        r = requests.get('https://youtube.com/c/' + channel_id + "/about/pbj=1", headers={
            "User-Agent": self.get_laptop_user_agent(),
            "X-YouTube-Client-Name": "1",
            "X-YouTube-Client-Version": "2.20200806.01.01"
        }, proxies=self.get_proxies()).json()
        payload = r[1]['response']
        return {
            "channel_title": self.extract_channel_title(payload),
            "channel_description": self.extract_channel_description(payload),
            "channel_keywords": self.extract_channel_keywords(payload),
            "channel_logo": self.extract_channel_logo(payload),
            "number_of_subscribers": self.extract_number_of_subscribers(payload),
            "number_of_views": self.extract_number_of_views(payload),
        }

    def scrap(self):
        tmp_list = []
        if 'profiles' in self.output_datasets:
            for account in self.input_config['accounts']:
                profile_data = self.scrape_channel_profile(account)
                tmp_list.append(profile_data)
            self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list, ignore_index=True)

    def quality_check(self):
        pass
