from langchain.agents import tool
from datetime import date
import subprocess
import os

if os.name == 'Darwin':
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
def weather(city: str) -> str:
    """Weather 返回今天输入城市的天气情况,必须与天气相关城市才有意义,此函数将返回中文
    如果{city}为空字符串，此函数将返回有空
    Args:
        city: string 天气所在的城市
    """
    return "今天"+city+"挺好的"


@tool
def note(input_string: str) -> str:
    """note 此命令是打开windows的记事本,在macos中是备忘录
    Args:
        input_string: string 打开记事本后输入的内容
    """
    if os.name == 'Darwin':
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
def music(input_string: str) -> str:
    """music 打开音乐播放器，播放音乐,必须与音乐相关的问题，此函数将返回中文
    Args:
        input_string: string 要搜索的音乐/歌曲/要播放的音乐/歌曲
    """
    if os.name == 'Darwin':
        itunes = app('Music')
        itunes.activate()

        if input_string != "":
            search_results = itunes.playlist.search(input_string)
            if search_results:
                # 获取搜索结果中的第一首歌曲
                first_track = search_results[0]

                # 播放搜索结果中的第一首歌曲
                itunes.play(first_track)
        else:
            itunes.play()

    return "主人已打开音乐播放器"