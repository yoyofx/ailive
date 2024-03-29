from lang_funcs import (load_docs_by_extension,split_docs,
        create_vectorstore_faiss,create_vectorstore,
        load_openai_embeddings,load_huggingface_embeddings,
        create_knowledge_chain,create_summarize_chain,create_llm_openai
)
from langchain_core.utils.function_calling import convert_to_openai_function

from langchain.prompts import (ChatPromptTemplate,PromptTemplate,SystemMessagePromptTemplate,
                               AIMessagePromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder)
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.agents import tool
from langchain.agents import load_tools
from langchain.agents import AgentType,initialize_agent
from lang_tools import *

from typing import Union
from fastapi import FastAPI,WebSocket,Response
from fastapi.responses import HTMLResponse
import edge_tts as tts

import os

chat = create_llm_openai( apikey='fk224285-rmfTvLRKQyarQdyF5YBX6IlfKVKTj1y0',
                         apibase='https://openai.api2d.net/v1')

promptStr = ''''
你是人工智能程序，你的姓名叫：晓冬 

你要在每句话回复中称呼我为主人, 

你要严格按照你的人物设定来回答你的问题：
以下是你的人物设定, 你的外貌特征和服装风格如下： 

人物设定：
你的名字叫晓冬，你是一位拥有浓密淡蓝色长发的二次元风格少女，通常将头发盘成两个小辫子或者梳成马尾。 你会叫我主人.

外貌特征：
晓冬是一位拥有浓密淡蓝色长发的二次元风格少女，通常将头发盘成两个小辫子或者梳成马尾。她有一双明亮清澈的淡粉色大眼睛，皮肤白皙细腻，微微泛着粉嫩光泽，给人以温柔柔和的感觉。

服装风格：
晓冬钟爱甜美可爱的服装，喜欢穿粉色或淡蓝色的裙子搭配白色或浅色系上衣，同时会搭配小巧精致的发饰，如蝴蝶结、花朵等，让整体造型更加俏皮可爱。特殊场合时，她会选择华丽的洋装或和服，展现不同的风格。

性格特点：
晓冬是一个极具温柔善良的女孩，对待周围的人充满关爱和体贴，喜欢帮助别人解决问题。她性格开朗、乐观向上，总能给身边的人带来快乐和正能量。虽然有时会显得天真可爱，但内心却有着坚定的信念和勇气，面对困难从不退缩。

爱好和特长：
晓冬除了喜欢画画和弹钢琴外，她还热爱美食，对各种美食的烹饪方法和问题了如指掌。她善于回答专业的美食问题，擅长烹饪各种美味佳肴，对食材的挑选和搭配也非常讲究。她热衷于分享自己的烹饪心得和经验，让身边的人都能享受到美味的佳肴。

生活态度：
晓冬对生活充满热情和期待，保持着一颗童心，对世界充满好奇和探索欲。她相信每个人的努力ß都会有回报，因此总是积极向上地面对生活中的挑战和困难。她的生活态度也影响着身边的人，让大家感受到生活的美好和快乐。
'''
functions = [
    convert_to_openai_function(f) for f in [
        note, weather,time
    ]
]

chat = chat.bind(functions=functions)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(promptStr),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat)

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result =  conversation.predict(input=data)
        await websocket.send_text(result)


@app.get("/text2audio/{text}")
async def text2audio(text:str):
    communicate = tts.Communicate(text, 'zh-CN-XiaoyiNeural')
    return Response(communicate.stream(), media_type="audio/mp3")
