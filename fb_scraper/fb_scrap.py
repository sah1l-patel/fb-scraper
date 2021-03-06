import urllib2
import json
import datetime
import csv
import time
import re

app_id = "**********"
app_secret = "*********" # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

page_id = 'nike'
start_date = datetime.datetime.today()
end_date = datetime.datetime.today()
diff_days = ((end_date + datetime.timedelta(1)) - (start_date - datetime.timedelta(1))).days

def testFacebookPageData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    print json.dumps(data, indent=4, sort_keys=True)
    

#testFacebookPageData(page_id, access_token)

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()


def testFacebookPageFeedData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id + "/feed" # changed
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    print json.dumps(data, indent=4, sort_keys=True)
    

#testFacebookPageFeedData(page_id, access_token)

def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed" 
    parameters = "/?since=%s&until=%s&fields=message,link,created_time,type,name,id,reactions.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (start_date,end_date,num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data
    

# test_status = getFacebookPageFeedData(page_id, access_token, 1)["data"][0]
# print json.dumps(test_status, indent=4, sort_keys=True)

def processFacebookPageFeedStatus(status):
    
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.
    
    # Additionally, some items may not always exist,
    # so must check for existence first
    
    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else dumb_to_smart_quotes(status['message']).encode('utf-8')
    link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else status['link']
    
    
    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.
    
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
    
    # Nested items require chaining dictionary keys.
    
    num_reactions = 0 if 'reactions' not in status.keys() else status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
    
    # return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
           status_published, num_reactions, num_comments, num_shares)

# processed_test_status = processFacebookPageFeedStatus(test_status)
# print processed_test_status

def scrapeFacebookPageFeedStatus(page_id, access_token, file):
    
    w = csv.writer(file)
    w.writerow(["run_datetime","start_date","end_date","diff_days","status_id", "status_message", "link_name", "status_type", "status_link",
       "status_published", "num_reactions", "num_comments", "num_shares"])
    
    has_next_page = True
    num_processed = 0   # keep a count on how many we've processed
    scrape_starttime = datetime.datetime.now()
    
    print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)
    
    statuses = getFacebookPageFeedData(page_id, access_token, 100)
    
    while has_next_page:
        for status in statuses['data']:
            w.writerow((scrape_starttime,start_date,end_date,diff_days) + processFacebookPageFeedStatus(status))
            
            # output progress occasionally to make sure code is not stalling
            num_processed += 1
            if num_processed % 1000 == 0:
                print "%s Statuses Processed: %s" % (num_processed, datetime.datetime.now())
                
        # if there is no next page, we're done.
        if 'paging' in statuses.keys() and 'next' in statuses['paging']:
            statuses = json.loads(request_until_succeed(statuses['paging']['next']))
        else:
            has_next_page = False
            
    
    print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)


def dumb_to_smart_quotes(string):
    """Takes a string and returns it with dumb quotes, single and double,
    replaced by smart quotes. Accounts for the possibility of HTML tags
    within the string."""

    # Find dumb double quotes coming directly after letters or punctuation,
    # and replace them with right double quotes.
    string = re.sub(r'([a-zA-Z0-9.,?!;:\'\"])"', r'\1&#8221;', string)
    # Find any remaining dumb double quotes and replace them with
    # left double quotes.
    string = string.replace('"', '&#8220;')
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around HTML
    # attributes (following =) and replace them with dumb quotes.
    string = re.sub(r'=&#8220;(.*?)&#8221;', r'="\1"', string)
    # Follow the same process with dumb/smart single quotes
    string = re.sub(r"([a-zA-Z0-9.,?!;:\"\'])'", r'\1&#8217;', string)
    string = string.replace("'", '&#8216;')
    string = re.sub(r'=&#8216;(.*?)&#8217;', r"='\1'", string)
    return string

def do_scraping(response):
    scrapeFacebookPageFeedStatus(page_id, access_token, response)
    return ('%s_facebook_statuses.csv' % page_id)
