from APIWrapper.OAuth import OAuth2
from APIWrapper.apPy import apPy
from PythonSaver.PythonSaver import load_dill

client_key = 'XXX'
client_secret = 'XXX'

def authorize_oauth():
    o2 = OAuth2(
        base_url='https://accounts.spotify.com',
        client_key=client_key,
        client_secret=client_secret,
        response_type='code',
        redirect_url='https://spotify.com'
    )

    # o2.authorize(endpoint='/authorize')
    # return o2

def create_api(oauth):
    api = apPy(
        base_url='https://api.spotify.com/v1'
    )
    api.add_endpoint(
        endpoint_name='search',
        endpoint='/search',
        protocol='GET',
        header={'Authorization': 'Bearer {0}'.format(oauth.access_token)}
    )
    print(oauth.access_token)
    return api

o = authorize_oauth()
# o = load_dill('spotify_oauth.dl')
# api = create_api(o)
# s = api.search(q='Green Day', type='track')
