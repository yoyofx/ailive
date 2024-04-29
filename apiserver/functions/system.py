import platform
from datetime import date

system = platform.system()

if system == "Darwin":
    from appscript import app



def today() -> str:
    """返回今天的日期    
    """

    return str(date.today())

def tomorrow() -> str:
    """返回明天的日期
    
    """
    return str(date.today() + 1)