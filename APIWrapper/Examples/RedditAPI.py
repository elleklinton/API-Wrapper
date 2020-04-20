import urllib.request as request
import json
import datetime
import webbrowser


class JSON: None


def create_query(base_url='http://api.pushshift.io/reddit/submission/search/?', arg_dict={}):
    query = base_url
    for key, value in arg_dict.items():
        query = query + '&{}={}'.format(key, value)
    return query

def query_creator(subreddit, start, end, size):
    params = {
        'after': start,
        'before': end,
        'sort_type': 'score',
        'sort' : 'desc',
        'subreddit': subreddit,
        'size' : size
    }
    return create_query(arg_dict=params)

def get_json_dict(url):
    response = request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))
    return data['data']

def convert_dict_to_object(dictionary):
    json_obj = JSON()
    for key, value in dictionary.items():
        if isinstance(value, dict):
            value = convert_dict_to_object(value)
        setattr(json_obj, key, value)
    return json_obj

def json_list_to_objs(json_list):
    lst = []
    for j in json_list:
        lst.append(convert_dict_to_object(j))
    return lst

def top_posts_from_subreddit(subreddit, start, end, size=100):
    q = query_creator(subreddit, start, end, size)
    posts = json_list_to_objs(get_json_dict(q))
    return posts


def display_images_from_objects(objects, limit=10):
    count = 0
    browser = webbrowser.Chrome()
    browser.open_
    for post in objects:
        count += 1
        if count >= limit: break
        browser.


if __name__ == '__main__':
    start = int((datetime.datetime.now() - datetime.timedelta(days=368)).timestamp())
    end = int((datetime.datetime.now() - datetime.timedelta(days=365)).timestamp())

    p = top_posts_from_subreddit('whitepeopletwitter', start, end)