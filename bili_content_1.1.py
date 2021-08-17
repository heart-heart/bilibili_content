import requests
import re
import time
import random
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
def get_content(url,oid):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    data_json = response.json()
    replies_count = data_json['data']['cursor']['all_count']
    print('评论总数：' + str(replies_count))
    if data_json['data']['replies'] !=None:
        page = 1
        replies = data_json['data']['replies']
        for rep in replies:
            uname = rep['member']['uname']
            print(uname + ':' + rep['content']['message'] + '(' + rep['reply_control']['sub_reply_title_text'] + ')')
            rep_replies = rep['replies']
            if rep_replies != None:
                replies_url = 'https://api.bilibili.com/x/v2/reply/reply?pn={page}&type=1&oid={oid}&ps=10&root={root}'
                root = rep_replies[0]['root']
                # print(root)
                replies_url = replies_url.format(page=page,root=root,oid=oid)
                # print(replies_url)
                time.sleep(random.randint(1,5))
                reply_response = requests.get(replies_url, headers=headers)
                reply_json = reply_response.json()
                list_reply = reply_json['data']['replies']
                count = reply_json['data']['page']['count']
                size = reply_json['data']['page']['size']
                if count/size == 0:
                    page_num = count/size
                else:
                    page_num = count//size + 1
                for li in list_reply:
                    print(li['member']['uname'] + "   " + '回复' + '    ' + uname + ':' + li['content']['message'])
                if count > size:
                    for pn in range(page + 1, page_num + 1):
                        replies_url = replies_url.replace('pn='+str(pn-1),'pn='+str(pn))
                        reply_response_pn = requests.get(replies_url, headers=headers)
                        reply_json_pn = reply_response_pn.json()
                        list_reply_pn = reply_json_pn['data']['replies']
                        for list_pn in list_reply_pn:
                            print(list_pn['member']['uname'] + "   " + '回复' + '    ' + uname + ':' + list_pn['content']['message'])
    else:
        print('结束爬取')
        sys.exit(0)
if __name__ == '__main__':
    #BV1oL411E7eR
    start_url = 'https://www.bilibili.com/video/BV1oL411E7eR'
    bv = start_url.split('/')[-1]
    url = 'https://api.bilibili.com/x/v2/reply/main?next=0&type=1&oid={oid}&mode=3&plat=1&_=1629184010686'
    response = requests.get(start_url,headers=headers)
    response.encoding = 'utf-8'
    page_text = response.text #获取主页面
    ex = '"{num}":{{"aid":(.*?),'.format(num = bv) #通过正则获取aid
    aid = re.findall(ex,page_text)[0]
    url = url.format(oid = aid)
    get_content(url=url,oid=aid)


    