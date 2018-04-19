#import urllib
from urllib.request import urlopen
import json
import requests
import time
import csv
import datetime

access_token="EAACEdEose0cBAMRMFuGYsYNvfDlfmf1oew8DBFNUEplCIPU9wIOQ3eq4C2WmR0F2KOg4AjFZB44OP1xHSw0LGuHh0J7fZBJxQF7xxRBS3AL6iAYcTanRTDsP2Qsq11nwhtZB1ZC4J7Bf2y0y5XdvS70dAzBHcTXH9lmJPc0ife5Ce27DHZC5g0nqZCFxZBQATkZD"

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

def getFBData(page_id,access_token,edge,lim_num):
    url1 = "https://graph.facebook.com/v2.11/"
    url2 = "%s/%s"%(page_id,edge)
    url4 = "&limit=%d"%(lim_num)
    url5 = "&access_token=%s"%(access_token)
    
    #adding datelimit
    tt = datetime.timedelta(6*365/12)
    dd = datetime.datetime.now()
    back_date = (dd-tt).strftime("%Y-%m-%d")
    cur_date = dd.strftime("%Y-%m-%d")
    url3 = "/?since=%s&until=%s"%(back_date,cur_date)
    
    url = url1+url2+url3+url4+url5
    
    data = getCurlData02(url)
    return data

def processFeedData(page_id,access_token,type_t,num_limit):
    csvfile = open('%s_fb_post_data.csv' % page_id, 'w', newline='')
    csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvf.writerow(["id","parent_id","created_time","message"])
    csvfile.close()
    
    next_page_available = True

    posts = getFBData(page_id,access_token,type_t,100)
    while next_page_available: 
        writecsvData(posts.get('data'))       
 
        if 'paging' in posts.keys():
            print('Parent Article:')
            print(posts['paging'])
            posts = getCurlData02(posts['paging']['next'])
        else:
            next_page_available=False

def writecsvData(posts):
    csvfile = open('%s_fb_post_data.csv' % page_id, 'a', newline='')
    csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    try:    
        for feed in posts:
            if feed.get('message')==None:
                continue
            
            csvf.writerow([feed['id'],'NULL',feed['created_time'],feed['message']])
            
            next_page_available = True
            
            comment = getFBData(feed['id'],access_token,'comments',100)
            while next_page_available: 
                commentdata = comment.get('data')
 
                if commentdata==None:
                    next_page_available=False

                for feed2 in commentdata:
                    csvf.writerow([feed2['id'],feed['id'],feed2['created_time'],feed2['message']])

                #if 'paging' in comment.keys():
                #    print('Child Article:')
                #    print(comment['paging'])
                #    comment = getCurlData02(comment['paging']['next'])
                #else:
                next_page_available=False

    except Exception as e:
        print('Error: ',e)
    
    finally:
        csvfile.close() 
    
if __name__=="__main__":
    page_id = input("Enter the page.id: ")
     
    processFeedData(page_id,access_token,'posts',100)

    print("Done")

