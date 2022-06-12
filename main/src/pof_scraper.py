# #this is no the live version. It contains dummy password. This is for testing only. this is  connected to cron job

#todo
#add ssh

import  bs4, sys, html2text, os , json
import mechanize
import ssl
from http.cookiejar import CookieJar


#uncomment these 2 lines of code if you get the below error. Some unicode encoding stuff
#UnicodeEncodeError: 'ascii' codec can't encode character u'|ufeff' in position 0: ordinal not in range(128)
#reload(sys)
#sys.setdefaultencoding('utf8')

stubFilename='carIdHashTable.json'
queryStringForViewMatches='http://www.pof.com/viewmatches.aspx?agelow=25&agehigh=35&miles=10&contacted=2&cmdSearch=Refine+Matches'
queryStringForBasicSearchPage='https://www.pof.com/basicsearch.aspx'
firstQueryString='https://www.pof.com/'
numberOfGoogleResults=1000
stubMessage='Hey, nice profile. Love your smile. Are you from Tucson originally?'
startValue=1
stubUrlForPof='http://www.pof.com/'
stubUrlForBasicSearchPage='http://www.pof.com/'
#stubUrlForTucsonCLInnerpages='http://tucson.craigslist.org/'
#stubUrlForPhxCLInnerpages='http://phoenix.craigslist.org/'
username=""
#the values can be manual, automatic, or both
transmission="both"
pwd=""



path = "/home/mithunpaul/allResearch/clscraper/main/src/"
#pathonLaptop
#path = "/home/mithunpaul/allResearch/clscraper/main/src/"




if(len(sys.argv)>1):
    username=sys.argv[1]
    pwd = sys.argv[2]
    #print("username:"+username)
   # print("pwd:" + pwd)

else:
    print("not enough arguments in Command Line. Exiting.")
    sys.exit(1)


def encodeAndwriteToOutputFile(textToWrite):
    target = open(stubFilename+'.txt', 'w+')
    target.write(html2text.html2text(textToWrite).encode('utf-8'))
    target.close()


def writeToOutputFile(textToWrite):
    target = open(stubFilename+'.txt', 'w+')
    target.write(textToWrite);
    target.close()

def AdduidToHashtable(uniqueId, localhtToCheck):
    localhtToCheck[uniqueId] = 1
#    print("length of hashtable inside checkAndadduidToHashtable is:"+`localhtToCheck.__len__()`)
    return localhtToCheck

def readFromJsonToHashtable(filename):
    # load from file:
    htMyTable={}
    with open(filename, 'r') as f:
        try:
            #print("inside child :length of hashtable that just came in is:"+`carIdHashTable.__len__()`)
            #carIdHashTable["test"] = 1
           # print("inside child :length of hashtable that just came in is:"+`carIdHashTable.__len__()`)
            htMyTable = json.load(f)
            #print("inside child :length of hashtable inside is:"+`htMyTable.__len__()`)
            #carIdHashTable=htMyTable
           # print("inside child :length of carIdHashTable inside is:"+`carIdHashTable.__len__()`)
        # if the file is empty the ValueError will be thrown
        except:
            carIdHashTable = {}
    return htMyTable

def send_from_basic_search_page(br,queryStringForViewMatches):
        already_sent_today={'viewprofile.aspx?profile_id=82509149':1}
        try:
            url = br.open(queryStringForViewMatches)
        except urllib2.HTTPError as e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError as e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException as e:
            print('HTTPException')
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())
        else:
            content = url.read()

        print("succesfully logged into pof")
        # parse the content into a format that soup understands
        soup = bs4.BeautifulSoup(content, "lxml")
        # for each of the hyperlinks in the page
        counter = 0
        for link in soup.find_all('a'):
            # print(link)
            classResult = link.get('class')
            if (classResult != None):
                    # if the class exists, get the link, if its not null
                    linkToNextPage = link.get('href')
                    if (linkToNextPage != None):
                        #check if this hyperlink has a profile id
                        if("profile_id" in  linkToNextPage):
                            #profile_id=74824023 is my own id
                            if  not ("profile_id=74824023" in linkToNextPage):
                                profilePageUrl = stubUrlForBasicSearchPage + linkToNextPage
                            # print(profilePageUrl)
                            # once you get the link to the person'as profile, open and go into that page.
                            else:
                                continue
                        else:
                            continue

                        try:
                            br.open(profilePageUrl)
                            # for f in br.forms():
                            # print f

                            # Select the first form (the first form is the quick message form)
                            br.select_form(nr=0)

                            # User credentials
                            br.form['message'] = stubMessage

                            # submit the text
                            if not(linkToNextPage in already_sent_today.keys()):
                                br.submit()
                                already_sent_today[linkToNextPage]=1
                            else:
                                continue

                            counter = counter + 1
                            print("sent message to " + profilePageUrl)

                        except Exception:
                            import traceback

                            print('generic exception: ' + traceback.format_exc())
                        # else:
                        # profilePageDetails = profilePage.read()

        print("done sending messages to " + str(counter) + "people")
        sys.exit(1)


def send_from_view_matches_page(br,queryStringForViewMatches):
    try:
        url = br.open(queryStringForViewMatches)
    except urllib2.HTTPError as e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError as e:
        print('URLError = ' + str(e.reason))
    except httplib.HTTPException as e:
        print('HTTPException')
    except Exception:
        import traceback
        print('generic exception: ' + traceback.format_exc())
    else:
        content = url.read()

    print("succesfully logged into pof")
    # parse the content into a format that soup understands
    soup = bs4.BeautifulSoup(content, "lxml")
    # for each of the hyperlinks in the page
    counter = 0
    for link in soup.find_all('a'):
        # print(link)
        classResult = link.text.lower()
        if (classResult != ""):
            if ("sign" in classResult):
                # if the class exists, get the link, if its not null
                linkToNextPage = link.get('href')
                if (linkToNextPage != None):
                    print("\n")
                    profilePageUrl = stubUrlForPof + linkToNextPage
                    # print(profilePageUrl)
                    # once you get the link to the person'as profile, open and go into that page.

                    try:
                        br.open(profilePageUrl)
                        # for f in br.forms():
                        # print f

                        # Select the first form (the first form is the quick message form)
                        br.select_form(nr=0)

                        # User credentials
                        br.form['message'] = stubMessage

                        # submit the text
                        # br.submit()
                        counter = counter + 1
                        print("sent message to " + profilePageUrl)

                    except urllib.HTTPError as e:
                        print('HTTPError = ' + str(e.code))
                    except urllib2.URLError as e:
                        print('URLError = ' + str(e.reason))
                    except httplib.HTTPException as e:
                        print('HTTPException')
                    except Exception:
                        import traceback

                        print('generic exception: ' + traceback.format_exc())
                    # else:
                    # profilePageDetails = profilePage.read()

    print("done sending messages to " + str(counter) + "people")
    sys.exit(1)

def writeToFileAsJson(myhashTable, filename):
    # save to file:
    with open(filename, 'w+') as f:
        json.dump(myhashTable, f)
    f.close()

def parseGResults(myQS):
    try:
        #code from http://stackoverflow.com/questions/20039643/how-to-scrape-a-website-that-requires-login-first-with-python
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = CookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.addheaders = [('User-agent', 'Chrome')]

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

        # The site we will navigate into, handling it's session
        response=br.open(myQS)
        print(response.read())

        send_from_view_matches_page(br, firstQueryString)

        # View available forms
        for f in br.forms():
            print(f)

        # Select the second (index one) form (the first form is a search query box)
        br.select_form(nr=0)

        # User credentials
        br.form['username'] = username
        br.form['password'] = pwd

        # Login
        br.submit()

        try:
            #note:queryStringForViewMatches already contains the clause: havent contacted before. You dont want to spam
            #someone you have already contacted and then get blocked
            if(useBasicSearchPage):
                send_from_basic_search_page(br,queryStringForBasicSearchPage)
            else:
                send_from_view_matches_page(br,queryStringForViewMatches)
        except:
            import traceback
            print('generic exception: ' + traceback.format_exc())

    except:
        import traceback
        print('generic exception: ' + traceback.format_exc())




cwd = os.getcwd()
print("current directory is:"+cwd)
# Now change the directory
# if(isRunningOnServer):
#     os.chdir( path )

# import requests
# #print(requests.get("https://www.pof.com/").content)
# import sys
# sys.exit()
parseGResults(firstQueryString)

