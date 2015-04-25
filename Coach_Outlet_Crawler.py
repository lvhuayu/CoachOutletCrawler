# This is a crawler to retrieve the picture of bag of coach outlet
#encoding=utf8
import cookielib, Cookie, urllib2, urllib
import re

class CoachOutletCrawler:
    
    cookies = cookielib.CookieJar() # the cookies of response will store in cookies
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies)) # create a url opener with cookie
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }

    def post(self, url, values):
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data, self.headers)
        self.cookies.add_cookie_header(request)
        response = self.opener.open(request)
        return response.read()

    def webpage_url_retrieval(self, html):
        pattern = re.compile(r"http://www.coachoutlet.com/store/default/the-april-23-event/women/handbags.html[\?p=\d]*")
        match = pattern.findall(html)
        urlset = set(match)
        return list(urlset)


    def picture_url_retrieval(self, html):
        pattern = re.compile(r"http://s7d2.scene7.com/is/image/Coach/.*\?")
        match = pattern.findall(html)
        urlset = set(match)
        return list(urlset)

    def download_picture(self, url):
        pattern = re.compile(r"http://s7d2.scene7.com/is/image/Coach/(f\d\d\d\d\d).*\?")
        match = pattern.match(url)
        if match:
            uid = match.group(1)
            file = "/Users/Jacob/Documents/CoachOutletImage/"+uid+".jpeg"
            urllib.urlretrieve(url, file)    

# create a instance of class CoachOutletCrawler
crawler = CoachOutletCrawler()

#verify the your email
request_url = "https://www.coachoutlet.com/store/default/customer/account/verifyCustomerType/"
values_verify = {'email' : 'xxxxx'} # input your email 
crawler.post(request_url, values_verify)

#login in
request_url = "https://www.coachoutlet.com/store/default/customer/account/loginPost/"
values_verify = {'email' : 'xxxxx', 'password':'xxxxx'} # input your email and password
crawler.post(request_url, values_verify)

#get the page of women's handbag page
request_handbag_url = "http://www.coachoutlet.com/store/default/the-april-23-event/women/handbags.html?LOC=TN2"
result = crawler.post(request_handbag_url, "")

#retrieve all urls of handbag pages
page_urls = crawler.webpage_url_retrieval(result)

#retrieve the pictures
number = 0
for url in page_urls:
    # get the html of this url
    html = crawler.post(url,"")
    # retrieve all urls of picture
    pic_urls = crawler.picture_url_retrieval(html)
    for url in pic_urls:
        print url
        number = number + 1
        crawler.download_picture(url)
print "***************"
print "Completed!"
print "The totle number is " + str(number)



