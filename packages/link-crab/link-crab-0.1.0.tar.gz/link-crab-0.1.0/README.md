# The Link Crab

A simple CLI tool which can crawl through your website and catch broken links, and can check user permissions to specific pages on your website.

## Workmode: Link gathering:
In this mode, you provide a starting url, and the Link Crab will crawl through the starting page, and all the page which is accessible thorugh links from that page and is in the same domain as the starting apge.
The program export the gathered links in a txt file, then exercise them, gathering response time and status code, and exporting these in a csv file.

## Workmode: Link access permission checking:
In this mode you provide a csv file with links to check, and wether those links should be accessible. The Link Crab will check every link in the list, determines if its accessible or not, and then assert the expected accessibilty to the actual accessibility. 
A link is considered accessible if the http response for a get request on the link has a status code under 400, and after all redirects, the url is equals of the starting url. 
(Most of the websites either give you a 404 or redirect to the sign-in page.)
*Maybe following the redirects is unnecessary, but I considered it safer*

## Session management:
In both workmode, you can provide login informations. The Link Crab opens up a Chrome browser with Selenium webdriver, and 

All reports are saved in the reports folder under a filder named by the domain name.
The configuration is done through a yaml config files.

## Installation

*soon...*

## Usage:
Simply use the command `link-crab/link-crab.py path/to/your/config.yaml` in the Link Crabs directory. All the configuration is done in the config files, which is expanded bellow.
If you want to use the sample flask mock app for testing, provide the `-t` flag.


### Usable config keys:
**starting_url**

    starting_url: http://127.0.0.1:5000

Gather the reachable links in the starting_url's page and all of its subpages.
After collecting all the links, the link exerciser load every in-domain url with a GET request, and measures 
status code, response time, response url after all redirects, and accessibility based on status code and response url

**path_to_link_perms**

    path_to_link_perms: testapp_member_access.csv

Test accessibility of provided links. The csv should have a link and a should-access column. 
asserts the link accessibility equals to provided should-access.
A link is accessible if the response status code<400, and after redirets the respone url equals the starting url
(some framework give a 404 for unaccessible pages or redriects to sign_in page)

**User**

    user:
        email: member@example.com
        email_locator_id: email
        login_url: http://127.0.0.1:5000/user/sign-in
        password: Password1
        password_locator_id: password
    
Login with the help of selenium webdriver (chromedriver). You need to provide the url of the login form, 
   and the id's of the email (or username) and password fields.