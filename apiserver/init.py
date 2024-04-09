from langchain.agents import AgentExecutor
from lang_funcs import ( create_llm_openai,create_llm_agent,read_toml  )
from lang_tools import *

# 初始化函数
def initialization(configName:str) -> AgentExecutor:
    config = read_toml(configName)

    promptStr = config["character"]["description"]
    chat = create_llm_openai( 
        apikey = config["openai"]["api_key"],
        apibase = config["openai"]["url"],
        max_tokens = config["openai"]["max_tokens"],
        model = config["openai"]["model"],
        )

    # tools = ["time","weather","note","music"]
    tools = config["character"]["tools"]
    llm_tools = []
    for tool in tools:
        llm_tools.append(globals()[tool])

    print(llm_tools)

    agent_executor = create_llm_agent(chat,promptStr,llm_tools)
    return agent_executor