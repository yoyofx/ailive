import os
from langchain_community.utilities import GoogleSerperAPIWrapper

def init_google_search(key:str):
    os.environ["SERPER_API_KEY"] = key
    print("init google search ......")


def google_search(query) -> str:
    search = GoogleSerperAPIWrapper()
    return search.run(query)