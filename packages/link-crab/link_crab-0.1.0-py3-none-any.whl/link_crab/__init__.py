import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tests.test_app import generate_mock_app
import time
import link_crab.session_manager
import link_crab.reporting
import link_crab.exercise_url
import link_crab.gather_links
import link_crab.csv_reader
import sys

from urllib.request import urlparse
import yaml
from datetime import datetime
import colorama

# Colorama init https://pypi.org/project/colorama/
colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
GRAY = colorama.Fore.LIGHTBLACK_EX
CYAN = colorama.Fore.CYAN
RESET = colorama.Fore.RESET




# CLI interface:
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Link-Crab: A link crawler and permission testing tool, written in Python",
        usage=f"""
        Provide a path for your config yaml file. 
        Usable {CYAN}config keys{RESET}:
            {CYAN}starting_url: http://127.0.0.1:5000{RESET}
                Gather the reachable links in the starting_url's page and all of its subpages.
                After collecting all the links, the link exerciser load every in-domain url with a GET request, and measures 
                status code, response time, response url after all redirects, and accessibility based on status code and response url
            
            {CYAN}path_to_link_perms: testapp_member_access.csv{RESET}
                Test accessibility of provided links. The csv should have a link and a should-access column. 
                asserts the link accessibility equals to provided should-access.
                A link is accessible if the response status code<400, and after redirets the respone url equals the starting url
                (some framework give a 404 for unaccessible pages or redriects to sign_in page)

            {CYAN}user:
                email: member@example.com
                email_locator_id: email
                login_url: http://127.0.0.1:5000/user/sign-in
                password: Password1
                password_locator_id: password{RESET}
                    Login with the help of selenium webdriver (chromedriver). You need to provide the url of the login form, 
                    and the id's of the email (or username) and password fields.
        """
        )
    parser.add_argument("config_yaml_path", metavar='config_yaml_path', type=str,
                        help="Path to the config yaml file.")
    parser.add_argument("-t" ,"--test", action='store_true', help="wind up the default test application for testing")

    args = parser.parse_args()
    config_yaml_path = args.config_yaml_path

    # setup:
    print('----------------setup---------------------')

    if args.test:
        generate_mock_app()

    starting_time = datetime.now()
    config = {}
    with open(config_yaml_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    user = None
    try:
        user = config['user']
    except:
        pass
    session = session_manager.make_session(user)

    starting_url = None
    try:
        starting_url = config['starting_url']
    except:
        pass

    path_to_link_perms = None
    try:
        path_to_link_perms = config['path_to_link_perms']
    except:
        pass

    links = set()

    links.add(starting_url)

    exit_value = 0
    exit_message =""

    # gathering:
    if starting_url:
        print('----------------gather links---------------------')
        checked_domain = urlparse(starting_url).netloc
        links.add(starting_url)
        links = gather_links.gather_links(session, links, checked_domain)

    # exercising:
        print('----------------Excercise links---------------------')
        link_db = []
        # remake the session, because crawling through the log-out link logs us out :D
        session = session_manager.make_session(user)
        for link in links:
            exercise_outcome = exercise_url.exercise_url(session, link)
            link_db.append(exercise_outcome)
            if exercise_outcome[1] > 400:
                exit_value = 1
                exit_message = exit_message + f"broken link found: {exercise_outcome[0]}\n"

        reporting.save_linkdb_to_csv(link_db, checked_domain)

        print('----------------REPORT: Excercised links---------------------')
        for link in link_db:
            print(f"[*] {link[0]} - {GREEN if link[1]==200 else RED} {link[1]} {RESET} - {GREEN if link[0]==link[4] else YELLOW} {link[4]} {RESET} - {link[2]} ms - accessible: {GREEN if link[3]==True else YELLOW} {link[3]} {RESET}")

    # permission checking:

    
    if path_to_link_perms:
        print('----------------permission checking---------------------')
        link_perm_db = []
        link_perms = csv_reader.read_link_perms(path_to_link_perms)
        checked_domain = urlparse(link_perms[0][0]).netloc
        session = session_manager.make_session(user)
        for link_perm in link_perms:
            outcome = (exercise_url.exercise_url(session, link_perm[0]))
            assertion_outcome = 'FAILED'
            if outcome[3] == link_perm[1]:
                assertion_outcome = 'PASSED'
            outcome = outcome + [link_perm[1]] + [assertion_outcome]
            link_perm_db.append(outcome)

        reporting.save_permdb_to_csv(link_perm_db, checked_domain)

        print('----------------REPORT: Checked permissions---------------------')
        for link in link_perm_db:
            if link[6] != 'PASSED':
                exit_value = 1
                exit_message = exit_message + f"Failed permission found: {link[0]}\n"
            print(f"[*] {link[0]} - {GREEN if link[1]==200 else RED} {link[1]} {RESET} - {GREEN if link[0]==link[4] else YELLOW} {link[4]} {RESET} - {link[2]} ms - accessible: {GREEN if link[3]==True else YELLOW} {link[3]} {RESET} - should-be?: {link[5]} - assert:{GREEN if link[6]== 'PASSED' else RED} {link[6]} {RESET}")

    # Exit:
    print(f"finished, exit:{exit_value}")
    print(exit_message)
    sys.exit(exit_value)



