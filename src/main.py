from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

response = simple_get("https://www.seek.co.nz/administrator-jobs/in-All-Wellington?sortmode=ListedDate")
html = BeautifulSoup(response, "html.parser")

for item in html.select("script"):
    if item.get("data-automation") == "server-state":
        # print(item)
        lines = item.get_text()

# Split lines and tidy up empty lines.
data = [line for line in lines.split('\n') if line.strip() != '']
print(data[0])
print(data[1])

# Base seek url for an individual job: https://www.seek.co.nz/job/36536458
# lines = 'thing window.SEEK_REDUX_DATA = {"dashboard": {"item": "nz"}}; hfhfhfh ksksks window.SEEK_ANALYTICS_DATA = {"thingy": "thing"};'
# pattern = r"{(.*)};"
# x = re.search(pattern, lines).group(0)
# print(x)
# clean = json.loads(x)
# pprint(clean)
