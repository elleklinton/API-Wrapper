from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth2Session
from APIWrapper.apPy import result_helper
import webbrowser
import urllib.parse as urlparse
from PythonSaver.PythonSaver import load_dill, save_dill

class OAuth1:
    #references Tweepy.auth
    def __init__(self, base_url='https://api.twitter.com/oauth/', client_key='XXX', client_secret='XXX', callback_url=None):
        self.base_url = base_url #+ '?&oauth_callback=oob'
        self.client_key = client_key.encode('ascii')
        self.client_secret = client_secret.encode('ascii')
        self.callback_url = callback_url
        self.session = OAuth1Session(self.client_key, self.client_secret, self.callback_url)

    def get_endpoint_url(self, endpoint):
        return self.base_url + endpoint

    def authorize(self, request_endpoint='request_token', auth_endpoint='authenticate', **kwargs):
        self.request_token = self.session.fetch_request_token(self.get_endpoint_url(request_endpoint), *kwargs)
        self.auth_url = self.session.authorization_url(self.get_endpoint_url(auth_endpoint), state=self.request_token)
        print('Open this URL in your browser:\n' + self.auth_url)
        webbrowser.open(self.auth_url)
        self.check_verifier()

    def check_verifier(self):
        pin = input('Enter PIN from browser: ').strip()
        try:
            self.session = OAuth1Session(
                client_key=self.client_key,
                client_secret=self.client_secret,
                callback_uri=self.callback_url,
                resource_owner_key=self.request_token['oauth_token'],
                resource_owner_secret=self.request_token['oauth_token_secret'],
                verifier=pin
            )
            self.tokens = self.session.fetch_access_token(self.get_endpoint_url('access_token'))
            self.tokens = result_helper(self.tokens)
        except Exception as err:
            print('error verifying pin:', err)

    @property
    def access_token(self):
        assert hasattr(self, 'tokens'), 'Authorization webflow was not completed successfully. Run self.authorize to authorize tokens.'
        return self.tokens.oauth_token

    @property
    def access_token_secret(self):
        assert hasattr(self, 'tokens'), 'Authorization webflow was not completed successfully. Run self.authorize to authorize tokens.'
        return self.tokens.oauth_token_secret


class OAuth2():
    def __init__(self, base_url='https://api.twitter.com/oauth', client_key='XXX', client_secret='XXX',
                 response_type='code', redirect_url=None):
        self.base_url = base_url
        self.client_key = client_key.encode('ascii')
        self.client_secret = client_secret.encode('ascii')
        self.response_type = response_type
        self.redirect_url = base_url
        if redirect_url:
            self.redirect_url = redirect_url

        self.session = OAuth2Session(self.client_key, redirect_uri=self.redirect_url)

        # self.session = OAuth1Session(self.client_key, self.client_secret, self.callback_url)

    def authorize(self, endpoint='/authorize', token_key='code', **kwargs):
        self.request_url, state = self.session.authorization_url(self.get_endpoint_url(endpoint), **kwargs)
        webbrowser.open(self.request_url)
        redirect_url = urlparse.urlparse(input(self.request_url + '\nGo to the above URL and then paste the URL you were redirected to:\n').strip())
        try:
            self.auth_token = urlparse.parse_qs(redirect_url.query)[token_key]
        except Exception as err:
            print('error parsing token:', err, redirect_url)
            self.auth_token = redirect_url

    @property
    def access_token(self):
        assert hasattr(self,
                       'auth_token'), 'Authorization webflow was not completed successfully. Run self.authorize to authorize tokens.'
        return self.auth_token[0]

    @property
    def access_token_secret(self):
        # assert hasattr(self,
        #                'tokens'), 'Authorization webflow was not completed successfully. Run self.authorize to authorize tokens.'
        return ''#self.tokens.oauth_token_secret



    def get_endpoint_url(self, endpoint):
        return self.base_url + endpoint


o2 = OAuth2(
    base_url='https://accounts.spotify.com',
    client_key='XXX',
    client_secret='XXX',
    response_type='code',
    redirect_url='https://spotify.com'
)

# a = o2.authorize()
# o2.base_url = 'https://api.spotify.com/v1/search'


# o = OAuth1(client_key='XXX', client_secret='XXX')
# o.authorize()
# save_dill(o, 'authorized_token.dl')
# print('Access token: {}\nAccess token secret: {}'.format(o.access_token, o.access_token_secret))


