# #this is no the live version. It contains dummy password. This is for testing only. this is  connected to cron job

#todo
#add ssh

import requests, bs4, sys, webbrowser, html2text, os , PyPDF2, urllib2, smtplib, re, json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import mechanize
import cookielib


#uncomment these 2 lines of code if you get the below error. Some unicode encoding stuff
#UnicodeEncodeError: 'ascii' codec can't encode character u'\ufeff' in position 0: ordinal not in range(128)
reload(sys)
sys.setdefaultencoding('utf8')

stubFilename='carIdHashTable.json'
queryStringStubForTucson='http://tucson.craigslist.org/search/cto?'
queryStringForViewMatches='http://www.pof.com/viewmatches.aspx?agelow=23&agehigh=99&miles=10&contacted=2&cmdSearch=Refine+Matches'
firstQueryString='http://www.pof.com/'
numberOfGoogleResults=1000
stubMessage='Hey, nice profile. Must say you have a very nice smile. Are you from Tucson originally?'
startValue=1
stubUrlForPof='http://www.pof.com/'
stubUrlForTucsonCLInnerpages='http://tucson.craigslist.org/'
stubUrlForPhxCLInnerpages='http://phoenix.craigslist.org/'
username=""
#the values can be manual, automatic, or both
transmission="both"
pwd=""
fromaddr="mithunpaul08@gmail.com"
toaddr="mithunpaul08@gmail.com"
#toaddr="jchebet@email.arizona.edu"
subjectForEmail= "Today's details of the used cars in tucson/phoenix area you asked for"
carbonCopy = "mithunpaul08@gmail.com"
#if on laptop dont switch path. This is required because cron runs as a separate process in a separate directory in chung
#turn this to true, if pushing to run on chung.cs.arizona.edu
isRunningOnServer=False;
firstTimeRun=False;


if(firstTimeRun):
    bodyOfEmail="Hi, \n Here is a list of all the cars found today in Craigslist. This is the very first email of craigslist scraping for used cars. Tomorrow onwards you will be shown only new hits that were not sent today. These are the parameters used for this query:\n\n"
else:
    bodyOfEmail="Hi,\n So the results you see below are what were newly found today. Everything else is same as what was sent yesterday. \nThese are the parameters used for this query:\n\n"


path = "/home/mithunpaul/allResearch/clscraper/main/src/"
#pathonLaptop
#path = "/home/mithunpaul/allResearch/clscraper/main/src/"

#toget to:email id and my gmail password from command line
if(len(sys.argv)>1):
    username=sys.argv[1]
    pwd = sys.argv[2]
    #print("username:"+username)
   # print("pwd:" + pwd)

else:
    print("not enough arguments in Command Line. Exiting.")
    sys.exit(1)



class myCar:
    min_price = ""
    max_price =""
    auto_make_model=""
    min_auto_year=""
    max_auto_year=""
    min_auto_miles=''
    max_auto_miles=''
    auto_title_status=''
    auto_transmission=''



#"Search Query attributes used to build the query string"
def fillSearchQueryAttributes(queryCar):
    queryCar.min_price = "1"
    queryCar.max_price ="6000"
    queryCar.auto_make_model="honda+%7C+toyota"
    queryCar.min_auto_year="2005"
    queryCar.max_auto_year="2016"
    queryCar.min_auto_miles='1'
    queryCar.max_auto_miles='110000'
    queryCar.auto_title_status='1'
    queryCar.auto_transmission='1'

def createQueryObject(queryStringStubToBuild, carObject):
    queryStringToSearch = str(queryStringStubToBuild)+"sort=priceasc&min_price="+carObject.min_price+\
                          "&max_price="+carObject.max_price+\
                          "&auto_make_model="+carObject.auto_make_model+\
                            "&min_auto_year="+carObject.min_auto_year+\
                                             "&max_auto_year="+carObject.max_auto_year+\
                                             "&min_auto_miles="+carObject.min_auto_miles+\
                                             "&max_auto_miles="+carObject.max_auto_miles+\
                                            "&auto_transmission="+carObject.auto_transmission+\
                                             "&auto_title_status="+carObject.auto_title_status
    if (transmission=="both"):
        queryStringToSearch=queryStringToSearch+"&auto_transmission="+`2`

    return queryStringToSearch

def sendEmail(listOfMyCars,carObject):
    finalMessageToSend=""
    if(listOfMyCars.__len__()==0):
        finalMessageToSend="hi, no new cars were found in today's search. Have a good day"
    else:
        queryResultsAsString="\n\n".join(listOfMyCars)
        bodyWithQueryDetails=createQueryObject(bodyOfEmail,carObject);
        bodyWithQueryDetailsreplacedAmbersand=bodyWithQueryDetails.replace("&", "\n")
        finalMessageToSend=bodyWithQueryDetailsreplacedAmbersand+"\n \nAnd the results are as follows:\n\n"+queryResultsAsString
    print("getting here at 32423")

    msg = "\r\n".join([
        "From: "+fromaddr,
        "To: " + toaddr,
        "CC: " + carbonCopy,
        "Subject:"+subjectForEmail,
        "",
        finalMessageToSend
    ])

    #print("getting here at 3687")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    #print("getting here at 8637")
    server.starttls()
    #print("getting here at 52895")
    server.login(gmailUsername, gmailPwd)
    #print("getting here at 5498")
    server.sendmail(fromaddr, toaddr, msg)
    #print("getting here at 68468")
    server.quit()
    print("done sending email to:"+toaddr)




def buildMessageBody(carObjectToBuildQuery):
    bodyOfEmail = "Hi, the details used for this query are as follows:"+carObjectToBuildQuery



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
    print("length of hashtable inside checkAndadduidToHashtable is:"+`localhtToCheck.__len__()`)
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
        except ValueError:
            carIdHashTable = {}
    return htMyTable


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
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.addheaders = [('User-agent', 'Chrome')]

        # The site we will navigate into, handling it's session
        br.open(myQS)

        # View available forms
        # for f in br.forms():
        #     print f

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
            url=br.open(queryStringForViewMatches)
            #url = urllib2.urlopen(queryStringToSearch)
        except urllib2.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
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
        for link in soup.find_all('a'):
            #print(link)
            classResult = link.get('class')
            if (classResult != None):
                if ("mi" in classResult):
                    # if the class exists, get the link, if its not null
                    linkToNextPage = link.get('href')
                    if (linkToNextPage != None):
                        print("\n")
                        profilePageUrl = stubUrlForPof + linkToNextPage
                        #print(profilePageUrl)
                        # once you get the link to the person'as profile, open and go into that page.


                        try:
                            br.open(profilePageUrl)
                            #for f in br.forms():
                                #print f

                            # Select the first form (the first form is the quick message form)
                            br.select_form(nr=0)

                            # User credentials
                            br.form['message'] = stubMessage


                            # submit the text
                            br.submit()
                            print("sent message to "+profilePageUrl)

                        except urllib2.HTTPError, e:
                            print('HTTPError = ' + str(e.code))
                        except urllib2.URLError, e:
                            print('URLError = ' + str(e.reason))
                        except httplib.HTTPException, e:
                            print('HTTPException')
                        except Exception:
                            import traceback
                            print('generic exception: ' + traceback.format_exc())
                        #else:
                            #profilePageDetails = profilePage.read()

        sys.exit(1)



    except:
        #print('generic exception: ')
        import traceback
        print('generic exception: ' + traceback.format_exc())
        #+sys.exc_info()[0])



cwd = os.getcwd()
print("current directory is:"+cwd)
# Now change the directory
if(isRunningOnServer):
    os.chdir( path )


parseGResults(firstQueryString)

