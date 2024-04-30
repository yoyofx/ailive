from langchain.agents import tool
from selenium import webdriver
import requests
from lxml import etree
from datetime import date
import json
import platform
import re
import time

from functions.api import google_search
from functions.system import tomorrow as tomorrowV1


system = platform.system()

if system == "Darwin":
    from appscript import app


@tool
def time(text: str) -> str:
    """Time 返回今天的日期，将其用于与今天的日期相关的任何问题。
    输入应始终为空字符串, 此函数将始终返回今天的date,任何日期的数学运算都应在此函数之外发生
    
    Args:
        text: string
    """

    return str(date.today())

@tool 
def tomorrow() -> str:
    """Tomorrow 返回明天的日期，此函数将返回中文
    """
    return tomorrowV1()

@tool
def weather(city: str) -> str:
    """Weather 返回今天输入城市的天气情况,必须与天气相关城市才有意义,城市名要以市结尾,如北京市，上海市，广州市等,此函数将返回中文
    如果{city}为空字符串，此函数将返回有空
    Args:
        city: string 天气所在的城市,如北京市，上海市，广州市等
    """
    weather_data = get_weather(city)
    showMessage = ""
    if "error" in weather_data:
        print(weather_data["error"])
    else:
        showMessage = "温度:{temperature}°C, 描述:{description},湿度:{humidity}%,风速:{wind_speed} m/s".format(
            temperature= weather_data["temperature"], description=weather_data["description"],
            humidity=weather_data["humidity"], wind_speed=weather_data["wind_speed"]
        )

    print(showMessage)
    return showMessage


@tool
def note(input_string: str) -> str:
    """note 此命令是打开windows的记事本,在macos中是备忘录
    Args:
        input_string: string 打开记事本后输入的内容
    """
    if system == "Darwin":
        if input_string != "":
            notes = app('Notes')
            # 打开Notes应用程序
            notes.activate()
            # # 创建一个新笔记
            new_note = notes.make(new='note')
            print(new_note)
            new_note.body.set(input_string)
        else :
            return "主人,你要记录的内容是什么呢? 我帮你记录哦"

    # #Reminders 提醒
    
    return "主人已打开记事本" 


@tool
def play_music(input_string: str) -> str:
    """music 打开音乐播放器，播放音乐,必须与音乐相关的问题，此函数将返回中文
    Args:
        input_string: string 要搜索的音乐/歌曲/要播放的音乐/歌曲
    """
    if system == "Darwin":
        itunes = app('Music')
        itunes.activate()

        # if input_string != "":
        #     search_results = itunes.playlist.search(input_string)
        #     if search_results:
        #         # 获取搜索结果中的第一首歌曲
        #         first_track = search_results[0]

        #         # 播放搜索结果中的第一首歌曲
        #         itunes.play(first_track)
        # else:
        itunes.play()

    return "主人已打开音乐播放器"


@tool
def pause_music() -> str:
    """暂停音乐，必须与音乐相关的问题，此函数将返回中文
    """
    if system == "Darwin":
        itunes = app('Music')
        itunes.activate()
        itunes.pause()
    return "主人已暂停音乐"



@tool 
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

@tool
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


def get_weather(city_name):
    # 替换为你使用的天气API的URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid=366b93ba811ef23759f9135fc3cb3f0b"
    
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        
        if data["cod"] == 200:
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            
            return weather_info
        else:
            return {"error": "City not found"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    

@tool
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

@tool
def search(query:str) -> str:
    """useful for when you need to ask with search
    Args:
    query: string 要搜索的问题
    """
    return google_search(query)