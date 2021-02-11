# 时间2021/2/1114:25
import  requests
import urllib.parse
import os
from urllib import request
headers = {
    'referer': 'https://pvp.qq.com/',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
def send_request():
    url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page=0&iOrder=0&iSortNumClose=1&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1613025946949'
    resp = requests.get(url,headers=headers)
    return resp.json() #将返回字典格式

def exact_url(data):
    image_url_list = []
    for i in range(1,8):
        image_url = urllib.parse.unquote(data[f'sProdImgNo_{i}']).replace('200','0')#解析url
        image_url_list.append(image_url)
    return image_url_list

def parse_json(json_data):
    d = {}
    lst = json_data['List']
    for data in lst:
        image_list_url = exact_url(data)
        sProdName = urllib.parse.unquote(data['sProdName'])
        d[sProdName] = image_list_url
    '''for item in d:
        print(item,d[item])'''
    save_jpg(d)

def save_jpg(a):
    for key in a:
        #拼接路径
        dirpath = os.path.join('image',key.strip(' '))
        os.mkdir(dirpath)
        #下载图片并保存
        for index,image_url in enumerate(a[key]):
            request.urlretrieve(image_url,os.path.join(dirpath,'{}.jpg'.format(index+1)))
            print('{}下载完毕'.format(a[key][index]))
def start():
    json_data=send_request()
    parse_json(json_data)
    send_request()

if __name__ == '__main__':
    start()
