# 时间2021/2/1220:35
import  requests
from urllib import parse
import urllib
from queue import   Queue
import  threading
import os
from urllib import  request
proxy = { #代理ip

    'http':'183.166.110.201:9999'

}
headers = {
    'referer': 'https://pvp.qq.com/',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

#获取url列表
def exact_url(data):
    image_url_list = []
    for i in range(1,8):
        image_url = urllib.parse.unquote(data[f'sProdImgNo_{i}']).replace('200','0')#解析url
        image_url_list.append(image_url)
    return image_url_list

#生产者线程
class Producer(threading.Thread):
    def __init__(self,page_queue,image_url_queue):
        super().__init__()
        self.page_queue = page_queue
        self.image_url_queue = image_url_queue
    def run(self):
        while not self.page_queue.empty(): # 如果page队列中的不会空
            page_url = self.page_queue.get()
            resp = requests.get(page_url,headers=headers,proxies=proxy) # 将取到的url发送请求
            json_data = resp.json() #转换成json格式
            #数据提取，遍历除图片url放入字典
            d = {}
            lst = json_data['List']
            for data in lst:
                image_list_url = exact_url(data)
                sProdName = urllib.parse.unquote(data['sProdName'])
                d[sProdName] = image_list_url
            #存储数据
            for key in d:
                # 拼接存储路径
                dirpath = os.path.join('image', key.strip(' '))
                if not os.path.exists('image'):
                    os.mkdir('image')
                if not os.path.exists(dirpath): #判断路径是否存在
                        os.mkdir(dirpath)
                # 下载图片并保存
                for index, image_url in enumerate(d[key]):
                    #生产图片的url,放入image_url队列中
                    self.image_url_queue.put({'image_path':os.path.join(dirpath,'{}.jpg'.format(index+1)),'image_url':image_url})

#消费者线程
class Customer(threading.Thread):
    def __init__(self,image_url_queue):
        super().__init__()
        self.image_url_queue = image_url_queue
    def run(self):
        while True:
            try:
                image_obj = self.image_url_queue.get(timeout=20) #数据阻塞20s后超时，抛出异常
                request.urlretrieve(image_obj['image_url'],image_obj['image_path'])
                print(f'{image_obj["image_path"]}下载完成')
            except:
                break

#启动线程函数
def start():
    page_queue = Queue(22)
    image_url_queue = Queue(1000)
    for i in range(0,3): #获取页面url
        page_url = f'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={i}&iOrder=0&iSortNumClose=1&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1613025946949'
        page_queue.put(page_url) #将每页url放入队列中

    #创建生产者线程对象
    for i in range(5):
        t = Producer(page_queue,image_url_queue)
        t.start()
    #创建消费者线程
    for i in range(10):
        t = Customer(image_url_queue)
        t.start()

if __name__ == '__main__':
    start()