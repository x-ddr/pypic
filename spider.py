import urllib.parse
import requests
import re
import json
import threading


thread_lock=threading.BoundedSemaphore(value=24)




def get_page(url):
    page=requests.get(url)
    page=page.content
    page=page.decode('utf-8')
    # print(page)
    return page

def pages_from_duitang(label):
    pages=[]
    url='https://www.duitang.com/napi/blog/list/by_search/?kw={}&type=feed&start={}'
    label=urllib.parse.quote(label)
    for index in range(0,720,24):
        u=url.format(label,index)
        print(u)
        page=get_page(u)
        pages.append(page)
    return pages


def findall_in_page(page,startpart,endpart):
    all_strings=[]
    end=0
    while page.find(startpart,end) != -1:
        start=page.find(startpart,end)+len(startpart)
        end=page.find(endpart,start)
        string=page[start:end]
        all_strings.append(string)
        # print(all_strings,"1")
    return all_strings



def pic_urls_from_pages(pages):
    pic_urls=[]
    for page in pages:
        urls=findall_in_page(page,'path":"','"')
        # print(urls)
        pic_urls.extend(urls)
    return pic_urls


def download_pices(url,n):
    r=requests.get(url)
    path='pic/'+str(n)
    with open(path,'wb')as f:
        f.write(r.content)
    thread_lock.release()

def main(label):
    pages=pages_from_duitang(label)
    pic_urls=pic_urls_from_pages(pages)
    # print(pic_urls)
    n=0
    for url in pic_urls:
        n+=1
        title1 = re.sub('https://c-ssl.duitang.com/uploads/', '', url)
        title2 = re.sub('item/', '', title1)
        title3 = re.sub('blog/', '', title2)
        title = re.sub('/', '-', title3)
        print('-----------正在下载第{}张图片-------------'.format(n)+title)
        thread_lock.acquire()
        t=threading.Thread(target=download_pices,args=(url,title))
        t.start()


main('壁纸')