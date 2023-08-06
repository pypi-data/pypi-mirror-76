from urllib.parse import quote

import requests

from roulette_russe.Scraper import Scraper


class TwitterScraper(Scraper):
    guest_token = ''
    guest_token_number_of_uses = 180

    def __init__(self, input_config, output_datasets, rr=None):
        super(TwitterScraper, self).__init__(input_config, output_datasets, rr)

    def get_guest_token(self):
        ua = self.get_laptop_user_agent()
        print("UA used to renew guest token for twitter: ", ua)
        self.guest_token_number_of_uses += 1
        if self.guest_token_number_of_uses > 30:
            r = requests.get('https://twitter.com/CNBC', proxies=self.get_proxies(), headers={
                'User-Agent': ua
            })
            self.guest_token_number_of_uses = 1
            self.guest_token = r.text.split('decodeURIComponent("gt=')[1].split(';')[0]
        return self.guest_token

    def get_num_id_from_username(self, username):
        print(username)
        r = requests.get('https://api.twitter.com/1.1/search/typeahead.json?q=' + username, proxies=self.get_proxies(),
                         headers={
                             'User-Agent': self.get_laptop_user_agent(),
                             'x-guest-token': self.get_guest_token(),
                             'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
                         })
        return str(r.json()['users'][0]['id'])

    def get_profile_data(self, twitter_numerical_id):
        while 1:
            try:
                r = requests.get('https://api.twitter.com/2/timeline/profile/' + twitter_numerical_id + '.json',
                                 headers={
                                     'User-Agent': self.get_mobile_user_agent(),
                                     'x-guest-token': self.get_guest_token(),
                                     'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
                                 })
                break
            except IndexError as e:
                print('TWITTER TRIED TO BLOCK ME')
                continue
        profile_data = r.json()['globalObjects']['users'][twitter_numerical_id]
        return {
            'twitter_internal_id': profile_data['id_str'],
            'username': profile_data['screen_name'],
            'company_tagline': profile_data['description'],
            'logo_link': profile_data['profile_image_url_https'],
            'followers_number': profile_data['followers_count'],
            'following_number': profile_data['friends_count'],
            'date_joined': profile_data['created_at'],
            'number_of_tweets': profile_data['statuses_count']
        }

    def get_tweets_data(self, twitter_numerical_id, account_name):
        tweets_list = []
        cursor_query = ''
        while 1:
            try:
                r = requests.get(
                    quote(
                        'https://api.twitter.com/2/timeline/profile/' + twitter_numerical_id + '.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&userId=' + twitter_numerical_id + '&count=20' + cursor_query,
                        safe='/:?=&'), proxies=self.get_proxies(),
                    headers={
                        'User-Agent': self.get_mobile_user_agent(),
                        'x-guest-token': self.get_guest_token(),
                        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
                    })
            except IndexError as e:
                print('TWITTER TRIED TO BLOCK ME')
                continue
            tweets = r.json()['globalObjects']['tweets']
            if tweets == {}:
                break
            entries_length = len(r.json()['timeline']['instructions'][0]['addEntries']['entries']) - 1
            cursor_query = '&cursor=' + \
                           r.json()['timeline']['instructions'][0]['addEntries']['entries'][entries_length]['content'][
                               'operation']['cursor']['value']
            for k in tweets:
                tweets_list.append({
                    'twitter_internal_id': twitter_numerical_id,
                    'tweet_date': tweets[k]['created_at'],
                    'tweet_url': 'https://twitter.com/' + account_name + '/status/' + k,
                    'comments_number': tweets[k]['reply_count'],
                    'retweets_number': tweets[k]['retweet_count'],
                    'likes_number': tweets[k]['favorite_count']
                })
            if len(tweets_list) > 1000:
                return tweets_list
        return tweets_list

    def scrap(self):
        tmp_list = []
        if 'profiles' in self.output_datasets:
            for account in self.input_config['accounts']:
                profile_data = self.get_profile_data(self.get_num_id_from_username(account))
                tmp_list.append(profile_data)
            self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list, ignore_index=True)
            print(self.output_datasets['profiles'].head())

        if 'tweets' in self.output_datasets:
            for account in self.input_config['accounts']:
                self.output_datasets['tweets'] = self.output_datasets['tweets'].append(
                    self.get_tweets_data(self.get_num_id_from_username(account), account),
                    ignore_index=True)

    def quality_check(self):
        pass
