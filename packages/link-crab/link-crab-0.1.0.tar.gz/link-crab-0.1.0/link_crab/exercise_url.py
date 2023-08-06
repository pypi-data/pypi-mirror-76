import requests
from urllib.request import urljoin, urlparse

import colorama

# Colorama init https://pypi.org/project/colorama/
colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

def exercise_url(session, url):
    '''
    Excersize url and gives back the following array:
    [0] visited url
    [1] status code
    [2] response time
    [3] accessible (bool)
    [4] returned url (after all redirects)
    args: 
        session: the session made by session_manager.py
        url: the url to be exercised
    '''
    if not check_url_validity(url):
        print(f"invalid link: {url}")
        return False
    try:
        resp = session.get(url) # maybe we should just use  allow_redirects=False for accessibility 
        accessible = resp.ok and resp.url == url
        outcome=[url,resp.status_code, int(resp.elapsed.total_seconds()*1000), accessible, resp.url] #should we change this to a dict? (depends on memory usage)
        print(f"[*] {outcome[0]} - {GREEN if outcome[1]==200 else RED} {outcome[1]} {RESET} - {GREEN if outcome[0]==outcome[4] else YELLOW} {outcome[4]} {RESET} - {outcome[2]} ms - accessible: {GREEN if outcome[3]==True else YELLOW} {outcome[3]} {RESET}")

    except:
        outcome=[url,err,err,False, err]
    return outcome


def check_url_validity(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


