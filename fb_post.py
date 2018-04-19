#import urllib
#from urllib.request import urlopen
import requests
import csv
import datetime

number_of_feeds = 0

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

#Parameters->(Page ID, access Token, Type of page like 'post''comment' etc, max limit of 1 chunk, parent ID of current
#request, csv file object
def processFeedData(page_id,access_token,type_t,num_limit,parent,csvf): 
    next_page_available = True

    posts = getFBData(page_id,access_token,type_t,num_limit)
    while next_page_available: 
        writecsvData(posts.get('data'),csvf,access_token,parent)       
 
        if 'paging' in posts.keys():
            #print('Type %s: '%(type_t))
            #print(posts['paging'])
            if posts.get('paging').get('next'):
                posts = getCurlData02(posts['paging']['next'])
            else:
                next_page_available=False 
        else:
            next_page_available=False

def writecsvData(posts,csvf,access_token,parent=None):
    try:
        global number_of_feeds
       
        for feed in posts:
            if feed.get('message')==None:
                continue
           
            #Keep track of progress of program
            number_of_feeds += 1
            if number_of_feeds%100 == 0:
                print("%d Feeds processed at %s"%(number_of_feeds,datetime.datetime.now()))            

            if parent==None: 
                csvf.writerow([feed['id'],'None',feed['created_time'],feed['message']])
                processFeedData(feed['id'],access_token,'comments',100,feed['id'],csvf)
            else:
                csvf.writerow([feed['id'],parent,feed['created_time'],feed['message']])
               
    except Exception as e:
        print('Error: ',e)  
    
if __name__=="__main__":
    page_id = input("Enter the page.id: ")
    access_token = input("Enter the access ID: ")
    
    csvfile = open('%s_fb_post_data.csv' % page_id, 'w', newline='')
    csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvf.writerow(["id","parent_id","created_time","message"])
     
    processFeedData(page_id,access_token,'posts',100,None,csvf)
    
    csvfile.close()

    print("Done")
    print("Total %d feeds processed"%(number_of_feeds))
