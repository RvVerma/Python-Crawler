from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    count=0
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data,links = parser.getLinks(url)
            print(" **Success!**")
            if data.find(word)>-1:
                count=count+1
                print("The word", word, "was found at", url)
            pagesToVisit = pagesToVisit + links
        except:
            print(" **Failed!**")
    if count==0:
        print("Word never found")
