
from langchain.agents import tool
from selenium import webdriver
import requests
from lxml import etree
from datetime import date
import json
import platform
import re
import time

system = platform.system()

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