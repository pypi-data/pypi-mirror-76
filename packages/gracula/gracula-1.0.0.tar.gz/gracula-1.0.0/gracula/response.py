from .oauth import TwitterOAuth
import urllib.parse


class TwitterResponse(object):
    TWITTER_API_URL = 'https://api.twitter.com/'

    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: str,
                 access_secret_key: str,
                 version='1.1'
                 ):

        self.oauth = TwitterOAuth(consumer_key, consumer_secret, access_token, access_secret_key)
        self.api_url = self.TWITTER_API_URL + version

    def get_followers_ids(self, screen_name=None, user_id=None, cursor=None, count=None):
        path = '/followers/ids.json'
        method = 'GET'

        params = {}

        if screen_name:
            params.update({'screen_name': str(screen_name)})
        elif user_id:
            params.update({'user_id': str(user_id)})

        if cursor:
            params.update({'cursor': str(cursor)})

        if count:
            params.update({'count': str(count)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_followers_list(self, screen_name=None, user_id=None, cursor=None, count=None):
        path = '/followers/list.json'
        method = 'GET'

        params = {}

        if screen_name:
            params.update({'screen_name': str(screen_name)})
        elif user_id:
            params.update({'user_id': str(user_id)})

        if cursor:
            params.update({'cursor': str(cursor)})

        if count:
            params.update({'count': str(count)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_users_lookup(self, screen_names=None, user_ids=None):
        path = '/users/lookup.json'
        method = 'GET'

        self.format_validation({
            'screen_names': screen_names,
            'user_ids': user_ids
        })

        if screen_names:
            params = {'screen_name': ','.join(screen_names)}
        elif user_ids:
            params = {'user_id': ','.join(map(str, user_ids))}
        else:
            raise ValueError('Please set screen_names or user_ids in the argument')

        return self.oauth.response(self.api_url + path, method, params)

    def get_users_show(self, screen_name=None, user_id=None):
        path = '/users/show.json'
        method = 'GET'

        if screen_name:
            params = {'screen_name': str(screen_name)}
        elif user_id:
            params = {'user_id': str(user_id)}
        else:
            raise ValueError('Please set screen_name or user_id in the argument')

        return self.oauth.response(self.api_url + path, method, params)

    def get_users_search(self, query, count=None, page=None):
        path = '/users/search.json'
        method = 'GET'

        params = {'q': urllib.parse.quote(query)}

        if count:
            params.update({'count': str(count)})

        if page:
            params.update({'page': str(page)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_friends_ids(self, screen_name=None, user_id=None, cursor=None, count=None):
        path = '/friends/ids.json'
        method = 'GET'

        if screen_name:
            params = {'screen_name': str(screen_name)}
        elif user_id:
            params = {'user_id': str(user_id)}
        else:
            raise ValueError('Please set screen_name or user_id in the argument')

        if cursor:
            params.update({'cursor': str(cursor)})

        if count:
            params.update({'count': str(count)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_friends_list(self, screen_name=None, user_id=None, cursor=None, count=None):
        path = '/friends/list.json'
        method = 'GET'

        if screen_name:
            params = {'screen_name': str(screen_name)}
        elif user_id:
            params = {'user_id': str(user_id)}
        else:
            raise ValueError('Please set screen_name or user_id in the argument')

        if cursor:
            params.update({'cursor': str(cursor)})

        if count:
            params.update({'count': str(count)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_user_timeline(self, screen_name=None, user_id=None, since_id=None, count=None, max_id=None):
        path = '/statuses/user_timeline.json'
        method = 'GET'

        if screen_name:
            params = {'screen_name': str(screen_name)}
        elif user_id:
            params = {'user_id': str(user_id)}
        else:
            raise ValueError('Please set screen_name or user_id in the argument')

        if since_id:
            params.update({'since_id': str(since_id)})

        if count:
            params.update({'count': str(count)})

        if max_id:
            params.update({'max_id': str(max_id)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_home_timeline(self, count=None, since_id=None, max_id=None):
        path = '/statuses/home_timeline.json'
        method = 'GET'

        params = {}

        if count:
            params.update({'count': str(count)})

        if since_id:
            params.update({'since_id': str(since_id)})

        if max_id:
            params.update({'max_id': str(max_id)})

        return self.oauth.response(self.api_url + path, method, params)

    def get_search_tweets(
            self,
            query,
            geocode=None,
            lang=None,
            locale=None,
            result_type=None,
            count=None,
            until=None,
            since_id=None,
            max_id=None):
        path = '/search/tweets.json'
        method = 'GET'

        params = {'q': urllib.parse.quote(query)}

        if geocode:
            params.update({'geocode': str(geocode)})

        if lang:
            params.update({'lang': str(lang)})

        if locale:
            params.update({'locale': str(locale)})

        if result_type:
            params.update({'result_type': str(result_type)})

        if count:
            params.update({'count': str(count)})

        if until:
            params.update({'until': str(until)})

        if since_id:
            params.update({'since_id': str(since_id)})

        if max_id:
            params.update({'max_id': str(max_id)})

        return self.oauth.response(self.api_url + path, method, params)

    @staticmethod
    def format_validation(data):
        if 'screen_names' in data and data['screen_names'] is not None and type(data['screen_names']) is not list:
            raise ValueError('Please put array in screen_names')

        if 'user_ids' in data and data['user_ids'] is not None and type(data['user_ids']) is not list:
            raise ValueError('Please put array in user_ids')
