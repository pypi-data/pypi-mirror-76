
import requests
import json

from roulette_russe.Scraper import Scraper


REFERER_URL = "https://www.instagram.com/"
BASE_URL = "https://www.instagram.com/"
LOGIN_URL = BASE_URL + "accounts/login/ajax/"
USER_AGENT_STORIES = "Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"


class InstagramScraper(Scraper):
    def __init__(self, input_config, output_datasets, username, password, rr=None):
        super(InstagramScraper, self).__init__(input_config, output_datasets, rr)
        self.session = requests.Session()
        self.session.cookies.set('ig_pr', '1')
        self.session.headers.update({"Referer": REFERER_URL, "user-agent": USER_AGENT_STORIES})
        req = self.session.get(BASE_URL)
        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
        login_data = {'username': username, 'password': password}
        login = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        login_text = json.loads(login.text)
        if login_text.get('authenticated') and login.status_code == 200:
            self.session.headers.update({'user-agent': USER_AGENT})
            print('OK')

    def query_main_infos(self, cookies, username):
        req = self.session.get("https://www.instagram.com/" + username, cookies=cookies).text
        return {
            "description": req.split('user":{"biography":"')[1].split('","')[0],
            "number_following": req.split('"edge_follow":{"count":')[1].split('},"')[0],
            "number_followers": req.split('"edge_followed_by":{"count":')[1].split('},"')[0],
            "full_name": req.split('"full_name":"')[2].split('","')[0],
            "username": req.split('"username":"')[2].split('","')[0],
            "twitter_internal_id": req.split('"id":"')[2].split('","')[0],
            "is_private_profile": req.split('"is_private":')[2].split(',"')[0],
        }

    def _query_followings(self, cookies, id, end_cursor=''):
        QUERY_FOLLOWINGS = BASE_URL + 'graphql/query/?query_hash=c56ee0ae1f89cdbd1c89e2bc6b8f3d18&variables={0}'
        QUERY_FOLLOWINGS_VARS = '{{"id":"{0}","first":50,"after":"{1}"}}'
        params = QUERY_FOLLOWINGS_VARS.format(id, end_cursor)
        req = self.session.get(QUERY_FOLLOWINGS.format(params), cookies=cookies).text
        if req is not None:
            payload = json.loads(req)['data']['user']['edge_follow']
            if payload:
                end_cursor = payload['page_info']['end_cursor']
                followings = []
                for node in payload['edges']:
                    followings.append(node['node']['username'])
                return followings, end_cursor
        return None, None

    def _query_followers(self,cookies, id, end_cursor=''):
        req = self.session.get(
            'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + id + '","include_reel":true,"fetch_mutual":true,"first":24,"after":"' + end_cursor + '"}',
            cookies=cookies).text
        if req is not None:
            payload = json.loads(req)['data']['user']['edge_followed_by']
            if payload:
                end_cursor = payload['page_info']['end_cursor']
                followers = []
                for node in payload['edges']:
                    followers.append(node['node']['username'])
                return followers, end_cursor
        return None, None

    def _query_commenters_of_post(self, cookies, post_short_code, end_cursor=''):
        QUERY_COMMENTERS = BASE_URL + 'graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={0}'
        QUERY_COMMENTERS_VARS = '{{"shortcode":"{0}","include_reel":true,"first":12,"after":"{1}"}}'
        params = QUERY_COMMENTERS_VARS.format(post_short_code, end_cursor)
        req = self.session.get(QUERY_COMMENTERS.format(params), cookies=cookies).text
        if req is not None:
            payload = json.loads(req)['data']['shortcode_media']['edge_media_to_comment']
            if payload:
                end_cursor = payload['page_info']['end_cursor']
                commenters = []
                for node in payload['edges']:
                    commenters.append(node['node']['owner']['username'])
                return commenters, end_cursor
        return None, None

    def _query_likers_of_post(self, cookies, post_short_code, end_cursor=''):
        QUERY_LIKERS = BASE_URL + 'graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={0}'
        QUERY_LIKERS_VARS = '{{"shortcode":"{0}","include_reel":true,"first":12,"after":"{1}"}}'
        params = QUERY_LIKERS_VARS.format(post_short_code, end_cursor)
        req = self.session.get(QUERY_LIKERS.format(params), cookies=cookies).text
        if req is not None:
            payload = json.loads(req)['data']['shortcode_media']['edge_liked_by']
            if payload:
                end_cursor = payload['page_info']['end_cursor']
                likers = []
                for node in payload['edges']:
                    likers.append(node['node']['username'])
                return likers, end_cursor
        return None, None

    def _query_posts(self, cookies, id, username, end_cursor=''):
        req = self.session.get(
            'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + id + '","first":24,"after":"' + end_cursor + '"}',
            cookies=cookies).text

        if req is not None:
            payload = json.loads(req)['data']['user']['edge_owner_to_timeline_media']
            if payload:
                end_cursor = payload['page_info']['end_cursor']
                posts = []
                for node in payload['edges']:
                    posts.append({
                        "username": username,
                        "is_video": node['node']['is_video'],
                        "short_code": node['node']['shortcode'],
                        "internal_id": node['node']['id'],
                        "link": "https://www.instagram.com/p/" + node['node']['shortcode'],
                        "comments_number": node['node']['edge_media_to_comment']['count'],
                        "likes_number": node['node']['edge_media_preview_like']['count'],
                        "timestamp": node['node']['taken_at_timestamp']
                    })
                return posts, end_cursor
            return None, None

    def query_posts(self, cookies, id, username):
        posts, end_cursor = self._query_posts(cookies, id, username)

        if posts:
            while True:
                for post in posts:
                    yield post
                if end_cursor:
                    posts, end_cursor = self._query_posts(cookies, id, username, end_cursor)
                else:
                    return

    def query_posts_likers(self, cookies, post_short_code):
        likers, end_cursor = self._query_likers_of_post(cookies, post_short_code)

        if likers:
            while True:
                for liker in likers:
                    yield liker
                if end_cursor:
                    likers, end_cursor = self._query_likers_of_post(cookies, post_short_code, end_cursor)
                else:
                    return

    def query_posts_commenters(self, cookies, post_short_code):
        commenters, end_cursor = self._query_likers_of_post(cookies, post_short_code)

        if commenters:
            while True:
                for commenter in commenters:
                    yield commenter
                if end_cursor:
                    commenters, end_cursor = self._query_commenters_of_post(cookies, post_short_code, end_cursor)
                else:
                    return

    def query_followers(self, cookies, id):
        followers, end_cursor = self._query_followers(cookies, id)

        if followers:
            while True:
                for follower in followers:
                    yield follower
                if end_cursor:
                    followers, end_cursor = self._query_followers(cookies, id, end_cursor)
                else:
                    return

    def query_followings(self, cookies, id):
        followings, end_cursor = self._query_followings(cookies, id)

        if followings:
            while True:
                for following in followings:
                    yield following
                if end_cursor:
                    followings, end_cursor = self._query_followings(cookies, id, end_cursor)
                else:
                    return

    def scrap(self):
        tmp_list_profiles=[]
        tmp_list_posts=[]
        tmp_list_followers = []
        tmp_list_following = []
        tmp_list_commenters = []
        tmp_list_likers = []
        for account in self.input_config['accounts']:
            profile_data = self.query_main_infos(cookies=self.cookies, username=account)
            tmp_list_profiles.append(profile_data)
        self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list_profiles, ignore_index=True)
        if 'posts' in self.output_datasets:
            for account in tmp_list_profiles:
                posts_data = self.query_posts(self.cookies, account['twitter_internal_id'], account['username'])
                tmp_list_posts += list(posts_data)
            self.output_datasets['posts'] = self.output_datasets['posts'].append(tmp_list_posts, ignore_index=True)
        if 'followers' in self.output_datasets:
            for account in tmp_list_profiles:
                followers_data = self.query_followers(self.cookies, account['twitter_internal_id'])
                tmp_list_followers.append({'account':account['username'], 'followers':list(followers_data)})
            self.output_datasets['followers'] = self.output_datasets['followers'].append(tmp_list_followers, ignore_index=True)
        if 'following' in self.output_datasets:
            for account in tmp_list_profiles:
                following_data = self.query_followings(self.cookies, account['twitter_internal_id'])
                tmp_list_following.append({'account':account['username'], 'following':list(following_data)})
            self.output_datasets['following'] = self.output_datasets['following'].append(tmp_list_following, ignore_index=True)
        if 'commenters' in self.output_datasets:
            for post in tmp_list_posts:
                commenters_data = self.query_posts_commenters(self.cookies, post['short_code'])
                tmp_list_commenters.append({'username': post['username'], 'post_short_code':post['short_code'], 'commenters':list(commenters_data)})
            self.output_datasets['commenters'] = self.output_datasets['commenters'].append(tmp_list_commenters, ignore_index=True)
        if 'likers' in self.output_datasets:
            for post in tmp_list_posts:
                likers_data = self.query_posts_likers(self.cookies, post['short_code'])
                tmp_list_likers.append({'username': post['username'], 'post_short_code':post['short_code'], 'likers':list(likers_data)})
            self.output_datasets['likers'] = self.output_datasets['likers'].append(tmp_list_likers, ignore_index=True)


    def quality_check(self):
        pass
