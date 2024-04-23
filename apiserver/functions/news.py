from selenium import webdriver
import requests
from lxml import etree
from datetime import date
import json
import platform
import re
import time

def baidu_hot_search() -> str:
    """查看/搜索/最新的 百度，新闻, 此函数将返回中文
    """
    urllib = 'https://top.baidu.com/board?tab=realtime'

    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }

    res = requests.get(urllib,headers=headers)

    nums = re.findall('<div class="index_1Ew5p c-index-bg.*?">  (\d+) </div>',res.text,re.S)
    titles = re.findall('<div class="c-single-text-ellipsis">(.*?)</div> ',res.text,re.S)
    details = re.findall('<div class="hot-desc_1m_jR large_nSuFU ">(.*?)<a',res.text,re.S)
    hotSearchs = re.findall('<div class="hot-index_1Bl1a"> (\d+) </div>',res.text,re.S)
    num = 15
    html_lists = zip(nums,titles,details,hotSearchs[:num])
    
    lines = []
    for num,title,detail,hotSearch in html_lists:
            lines.append(f"{num}. {title}")

    message = "\n".join(lines)
    return message



def weibo_hot_search() -> str:
    """查看/搜索/最新的 新浪微博，热搜，新鲜事，此函数将返回中文
    """
    # 获取json文件
    def hot_search():
        url = 'https://weibo.com/ajax/side/hotSearch'
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()['data']

    num = 20
    data = hot_search()
    if not data:
        print('获取微博热搜榜失败')
        
    # 获取热搜榜
    lines = [f"置顶:{data['hotgov']['word'].strip('#')}"]
    for i, rs in enumerate(data['realtime'][:num], 1):
        title = rs['word']
        try:
            label = rs['label_name']
            if label in ['新','爆','沸']:
                label = label
            else:
                label = ''
        except:
            label = ''
        lines.append(f"{i}. {title} {label}")
    message = "\n".join(lines)
    return message


def douban_movies() -> str:
    """查看/看看 最新有什么新电影,返回中文
    只返回前10个 电影名 (主演和电影类型不返回)
    """
    Header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
          'Referer': 'https://movie.douban.com/cinema/later/beijing/'}

    Url = 'https://movie.douban.com/cinema/nowplaying/beijing/'
    Reqs = requests.get(url=Url, headers=Header)
    jier = Reqs.text
    # print(jier)

    # 获取正在上映的Div下的list
    A_Html = etree.HTML(jier)
    Div_Html = A_Html.xpath('//*[@id="nowplaying"]//ul[@class="lists"]')[0]
    Li_Html = Div_Html.xpath('./li')
    messageList = []
    index = 1
    for limv in Li_Html:
        if index <= 15:
            title = limv.xpath('@data-title')[0].strip()
            score = limv.xpath('@data-score')[0].strip() 
            actors =  limv.xpath('@data-actors')[0].strip()  
            messageList.append(f"{index}.{title},评分:{score},演员:{actors}")
        index = index + 1
    message = "\n".join(messageList)
    return message