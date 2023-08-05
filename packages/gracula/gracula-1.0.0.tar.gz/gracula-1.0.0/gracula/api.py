from .response import TwitterResponse


class Api(object):
    TWITTER_API_URL = 'https://api.twitter.com/'

    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: str,
                 access_secret_key: str,
                 version='1.1'
                 ):
        self.twitter = TwitterResponse(consumer_key, consumer_secret, access_token, access_secret_key, version)

    def get_user(self, screen_name=None, user_id=None):
        response = self.twitter.get_users_show(screen_name, user_id)
        return response if response else None

    def get_users(self, query, count=None, page=None):
        response = self.twitter.get_users_search(query, count, page)
        return response if response else None

    def get_multiple_users(self, screen_names=None, user_ids=None):
        response = self.twitter.get_users_lookup(screen_names, user_ids)
        return response if response else None

    def get_follower_user_ids(self, screen_name=None, user_id=None, cursor=None, count=None):
        response = self.twitter.get_followers_ids(screen_name, user_id, cursor, count)
        return response if response else None

    def get_follower_user_list(self, screen_name=None, user_id=None, cursor=None, count=None):
        response = self.twitter.get_followers_list(screen_name, user_id, cursor, count)
        return response if response else None

    def get_follow_user_ids(self, screen_name=None, user_id=None, cursor=None, count=None):
        response = self.twitter.get_friends_ids(screen_name, user_id, cursor, count)
        return response if response else None

    def get_follow_user_list(self, screen_name=None, user_id=None, cursor=None, count=None):
        response = self.twitter.get_followers_list(screen_name, user_id, cursor, count)
        return response if response else None

    def get_user_timeline(self, screen_name=None, user_id=None, since_id=None, count=None, max_id=None):
        response = self.twitter.get_user_timeline(screen_name, user_id, since_id, count, max_id)
        return response if response else None

    def get_home_timeline(self, count=None, since_id=None, max_id=None):
        response = self.twitter.get_home_timeline(count, since_id, max_id)
        return response if response else None

    def get_tweets(self, query, geocode=None, lang=None, locale=None, result_type=None, count=None, until=None,
                   since_id=None, max_id=None):
        response = self.twitter.get_get_tweets(
            query, geocode, lang, locale, result_type, count, until, since_id, max_id)

        return response if response else None
