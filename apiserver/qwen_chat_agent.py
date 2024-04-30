from typing import Any, Dict, List, Optional, Type, Union, cast
import datetime
from qwen_agent.agents import Assistant,ReActChat
from qwen_tools import *


class QwenChatAgent():
    llm_cfg = {}
    historyCount = 0
    historyK = 3
    chat_messages = []
    last_message_time = None
    agnet = None
    def __init__(self,url,model:str="qwen:7b-chat",prompt:str="",tools:List=[],k:int=3):
        self.llm_cfg = {
            "model": model,
            "model_server": url,
            "generate_cfg": {
                "top_p": 0.9,
            }
        }
        self.historyK = k
        self.historyCount = 0
        self.agent = Assistant(llm=self.llm_cfg, system_message=prompt,function_list=tools)
        print(self.agent)
        
    def invoke(self,input: Dict[str, Any]):
        current_time = datetime.datetime.now()
        print(self.chat_messages)

        question = input["input"]
        # if self.historyCount > self.historyK:
        #     self.chat_messages = self.chat_messages[2:]  # delete input and output
        if question == '/清空' or question == '/clear':
            self.chat_messages = []
            return {"output": "我失忆了,o my god!"}
        if "几点" in question or "当前时间" in question:
            self.chat_messages.append({"role": "assistant", "content": "我失忆了,o my god!"})
            return {"output": current_time.strftime("%Y/%m/%d %H:%M:%S")  }

        if len(self.chat_messages) > 5: 
            self.chat_messages = []
        # question = "请详细回答以下问题：" + question
        self.chat_messages.append({'role': 'user', 'content': question})
        response = self.agent.run(messages=self.chat_messages)
        responses = []
        responses.extend(response)

        systemMessages = []

        if len(responses) > 0:
            responses = responses[-1]
        if len(responses) > 0:
            systemMessages = responses
            responses = responses[-1]
            # if len(responses) > 1 and responses[-2]["role"] == "function" and "error" not in responses[-2]["content"]:
            #     responses = responses[-2]
            # else :
            #     responses = responses[-1]

        self.last_message_time = current_time

        print(systemMessages)
        msgList = []
        msgList.extend(systemMessages)
        msgList.extend(self.chat_messages)
        self.chat_messages = msgList 
        return {"output": responses["content"]} 