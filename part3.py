# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

url = "https://www.michigandaily.com";
r = requests.get(url);
soup = BeautifulSoup(r.text, 'html.parser');
mostReadList = soup.find("div", {"class": "pane-mostread"});
mostReadTitles = mostReadList.find_all('a');

print ("Michigan Daily -- MOST READ")
for title in mostReadTitles:
    articleName = title.contents[0];
    articleLink = url + title.get('href');
    subSoupR = requests.get(articleLink);
    subSoup = BeautifulSoup(subSoupR.text, 'html.parser');
    authorLink = subSoup.find("div", {"class": "link"});
    if(authorLink):
        author = authorLink.find('a').contents[0]
    else:
        author = subSoup.find("p", {"class": "info"}).contents[0];
    print (articleName)
    print ("by " + author)
