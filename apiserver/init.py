from langchain.agents import AgentExecutor
from lang_funcs import ( create_llm_openai,create_llm_agent,read_toml  )
from lang_tools import *
from qwen_chat_agent import QwenChatAgent

# 初始化函数
def initialization(configName:str) -> any:
    config = read_toml(configName)
    print("Create LLM ......")
    print("LLM API: " + config["openai"]["url"])
    print("LLM Model: " + config["openai"]["model"])
    agentMode = config["agent"]["mode"]
    print("Agent Mode: " + agentMode)

    promptStr = config["character"]["description"]
    tools = config["character"]["tools"]

    print("Create Agent ......")
    if agentMode == "langchain":    
        chat = create_llm_openai( 
            apikey = config["openai"]["api_key"],
            apibase = config["openai"]["url"],
            max_tokens = config["openai"]["max_tokens"],
            model = config["openai"]["model"],
        )
        llm_tools = []
        for tool in tools:
            llm_tools.append(globals()[tool])
        print("loaded tools ......")
        print(llm_tools)
        agent_executor = create_llm_agent(chat,promptStr,llm_tools)

    elif agentMode == "qwen":
        agent_executor = QwenChatAgent(url=config["openai"]["url"],model=config["openai"]["model"],prompt=promptStr,tools=tools,k=5)
        
    return agent_executor