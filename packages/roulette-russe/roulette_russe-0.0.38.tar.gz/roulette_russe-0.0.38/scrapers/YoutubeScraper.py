import requests

from roulette_russe.Scraper import Scraper


class YoutubeScraper(Scraper):
    def __init__(self, input_config, output_datasets, rr=None):
        super(YoutubeScraper, self).__init__(input_config, output_datasets, rr)

    def extract_channel_title(self, payload):
        return payload['metadata']['channelMetadataRenderer']['title']

    def extract_channel_description(self, payload):
        return payload['metadata']['channelMetadataRenderer']['description']

    def extract_channel_keywords(self, payload):
        return payload['metadata']['channelMetadataRenderer']['keywords'].split(' ')

    def extract_channel_logo(self, payload):
        return payload['metadata']['channelMetadataRenderer']['avatar']['thumbnails'][0]['url']

    def extract_number_of_subscribers(self, payload):
        text_n_subscribers = payload['header']['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText'].split(
            '\xa0')
        if len(text_n_subscribers) == 3:
            return text_n_subscribers[0:2]
        else:
            return text_n_subscribers[0]

    def extract_number_of_views(self, payload):
        result = 0
        for tab in payload['contents']['twoColumnBrowseResultsRenderer']['tabs']:
            if (tab['tabRenderer']['title'] == "À propos") or (tab['tabRenderer']['title'] == "About"):
                result = int(tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer'][
                              'contents'][0]['channelAboutFullMetadataRenderer']['viewCountText'][
                              'simpleText'].replace('\xa0vues', '').replace('\u202f', ''))
                break
        return result

    def scrape_channel_profile(self, channel_id):
        r = requests.get('https://youtube.com/c/' + channel_id + "/about?pbj=1", headers={
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
