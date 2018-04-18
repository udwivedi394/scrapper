#import urllib
from urllib.request import urlopen
import json
import requests
import time
import csv
import datetime


access_token="EAACEdEose0cBAMjqxovNoPOokjw5lG1W54jTZBZCAGWksmD3f3OsoMgU3Y8nA22I4WWPOIXZCSu0vC3HNdHoZATZBJ7GSLwmQCauRZAvP6WrfaPlmWup3AZBPeM1PoFIrafO0NoO6FLZA3ZCSJ8nyt9i7JEDKXFGcSXJpysJ2rkPhQBgPLtLWQJ8pEU0pOoARCtoDVGucn2bckAZDZD"


def getCurlData02(url):
    end = False
    while end==False:
        try:
            response = requests.get(url)
            end=True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Retrying...")
    return response.json()

def getFBData(page_id,access_token,edge):
    url1 = "https://graph.facebook.com/v2.11/"
    url2 = "%s/%s"%(page_id,edge)
    url3 = "&access_token=%s"%(access_token)
    
    #adding datelimit
    tt = datetime.timedelta(6*365/12)
    dd = datetime.datetime.now()
    back_date = (dd-tt).strftime("%Y-%m-%d")
    cur_date = dd.strftime("%Y-%m-%d")
    url4 = "/?since=%s&until=%s"%(back_date,cur_date)
    
    url = url1+url2+url4+url3
    
    data = getCurlData02(url)
    return data.get('data')
    
if __name__=="__main__":
    page_id = input("Enter the page.id: ")

    with open('%s_fb_post_data.csv' % page_id, 'w', newline='') as csvfile:
        csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvf.writerow(["id","parent_id","created_time","message"])
 
        posts = getFBData(page_id,access_token,'posts')
        for feed in posts:
            
            if feed.get('message')==None:
                continue
            
            csvf.writerow([feed['id'],'NULL',feed['created_time'],feed['message']])
            commentdata = getFBData(feed['id'],access_token,'comments')
            
            if commentdata==None:
                continue
            
            for feed2 in commentdata:
                csvf.writerow([feed2['id'],feed['id'],feed2['created_time'],feed2['message']])

        print("Done")
