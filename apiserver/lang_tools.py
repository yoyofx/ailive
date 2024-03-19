from langchain.agents import tool
from datetime import date


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
    """Weather 返回今天输入城市的天气情况,此函数将返回中文

    Args:
        city: string
    """
    return "今天"+city+"挺好的"


@tool
def note(input_string: str) -> str:
    """note 此命令是打开windows的记事本,在macos中是备忘录
    """
    print("func 打开记事本")
    return "主人已打开记事本"