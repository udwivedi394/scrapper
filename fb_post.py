#import urllib
from urllib.request import urlopen
import json
import requests
import time
import csv


access_token="EAACEdEose0cBAG1HrmC1VQWkXxKwwsZCpLFAhHfLR2i9jW8B1CMt2lkbLg4HigkX8gu1OoQg9L8BbmFiupljLcZB1ZB4xzzG4PjWj6zHvTGALqaU71kiD3ZA8PBKuGZCxCeLi3XwyYDuh6gPooHibeysoaajXESWZARzjMRj7aL5oXP4y34oP3r5DayYhmMfkZD"

def getCurlData(url):
    #req = urllib2.Request(url)
    #response = urllib2.urlopen(req)
    response = urlopen(url)
    if response.getcode() == 200:
        print("Printing Here: ")
        print(response.read().decode('utf-8'))
        return response.readall().decode('utf-8').json()
    return response.read()

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
    url3 = "/?access_token=%s"%(access_token)
    
    url = url1+url2+url3
    
    #data = json.loads(getCurlData02(url))
    data = getCurlData02(url)
    return data.get('data')
    
if __name__=="__main__":
    page_id = input("Enter the page.id: ")

    with open('%s_fb_post_data.csv' % page_id, 'w', newline='') as csvfile:
        csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #ofile.write(','.join(["id","parent_id","created_time","message"]))
        #print(','.join(["id","parent_id","created_time","message"]))
        csvf.writerow(["id","parent_id","created_time","message"])
 
        posts = getFBData(page_id,access_token,'posts')
        for feed in posts:
            if feed.get('message')==None:
                continue
            #f.writerow(feed['id'],'NULL',feed['created_time'],feed['message'])
            #print(','.join([feed['id'],'NULL',feed['created_time'],feed['message']]))
            csvf.writerow([feed['id'],'NULL',feed['created_time'],feed['message']])
            commentdata = getFBData(feed['id'],access_token,'comments')
            if commentdata==None:
                continue
            for feed2 in commentdata:
                csvf.writerow([feed2['id'],feed['id'],feed2['created_time'],feed2['message']])

        print("Done")
