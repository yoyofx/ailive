from qwen_agent.tools.base import BaseTool, register_tool
from typing import Any, Dict, List, Optional, Type, Union, cast
import urllib.parse
import json5
from datetime import datetime
from functions.news import *
from functions.weater import *
from functions.system import *

@register_tool('weather')
class GetWeather(BaseTool):
    description = '返回今天输入城市的天气情况,必须与天气相关城市才有意义,城市名要以市结尾,如北京市，上海市，广州市等'
    parameters = [{
        'name': 'city',
        'type': 'string',
        'description': '天气所在的城市,如北京市，上海市，广州市等',
        'required': True
    }]

    def call(self, params: Union[str, dict], **kwargs) -> str:
        print(params)
        params = params.replace("{{","{")
        params = params.replace("}}","}")
        params = self._verify_json_format_args(params)
        city = params['city']        
        city = urllib.parse.quote(city)
        return weather(city)
    
@register_tool('time')
class WhatTime(BaseTool):
    description = '返回今天的日期'

    def call(self, params: str, **kwargs) -> str:     
        return today()
    
@register_tool('tomorrow')
class Tomorrow(BaseTool):
    description = '返回明天的日期'
    def call(self, params: str, **kwargs) -> str:     
        return tomorrow()
    
@register_tool('baidu_hot_search')
class BaiduHotsearch(BaseTool):
    description = '详细回答有关新闻的相关问题并返回全部列表 最新的 / 百度 / 新闻 / news'
    def call(self, params: Union[str, dict,None], **kwargs) -> str:     
        return baidu_hot_search()
    
@register_tool('weibo_hot_search')
class WeiboHotSearch(BaseTool):
    description = '详细回答热搜相关问题并返回全部列表 , 最新的 / 新浪 / 微博 / 热搜 / 新鲜事'
    def call(self, params: Union[str, dict,None], **kwargs) -> str:     
        return weibo_hot_search()
    

@register_tool('douban_movies')
class WeiboHotSearch(BaseTool):
    description = '最新 新电影 / 正在上映 / 电影 '
    def call(self, params: Union[str, dict,None], **kwargs) -> str:     
        return douban_movies()