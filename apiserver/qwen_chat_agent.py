from typing import Any, Dict, List, Optional, Type, Union, cast
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
        current_time = datetime.now()

        question = input["input"]
        # if self.historyCount > self.historyK:
        #     self.chat_messages = self.chat_messages[2:]  # delete input and output
        if question == '/清空' or question == '/clear':
            self.chat_messages = []

        # 根据回复时间清空chat_message > 30s
        if self.last_message_time is None or (current_time - self.last_message_time).total_seconds() > 30:
            self.chat_messages = []  # Clear chat messages

        self.chat_messages.append({'role': 'user', 'content': question})
        response = self.agent.run(messages=self.chat_messages)
        responses = []
        responses.extend(response)
        print(responses)

        if len(responses) > 0:
            responses = responses[-1]
        if len(responses) > 0:
            responses = responses[-1]
        # self.chat_messages.append(responses["content"])
        # self.historyCount = self.historyCount + 1
        self.last_message_time = current_time

        return {"output": responses["content"]} 