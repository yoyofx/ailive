from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.schema.language_model import BaseLanguageModel
from lang_funcs import ( create_llm_openai,create_llm_agent,read_toml )
from lang_tools import *

from typing import Union
from fastapi import FastAPI,WebSocket
from fastapi.responses import HTMLResponse,StreamingResponse,JSONResponse
import edge_tts as tts
from pydantic import BaseModel
import tomllib



config = read_toml("./config.toml")

chat = create_llm_openai( apikey=config["openai"]["api_key"],
                         apibase=config["openai"]["url"])

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

config = read_toml("./config.toml")

chat = create_llm_openai( apikey=config["openai"]["api_key"],
                         apibase=config["openai"]["url"])

tools = ["time","weather","note","music"]
llm_tools = []
for tool in tools:
    llm_tools.append(globals()[tool])

print(llm_tools)

agent_executor = create_llm_agent(chat,promptStr,llm_tools)

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
        result = agent_executor.invoke({"input": data })
        await websocket.send_text(result["output"])


class Text2Audio(BaseModel):
    text: str

def ApiResult(data:Union[list,dict,str] = None, message:str = "Success", success:bool = True):
    return JSONResponse(
        status_code=200,
        content= {
            "data": data or {}, 
            "message": message, 
            "success": success})


@app.post("/text2audio/",)
async def text2audio(request:Text2Audio):
    communicate = tts.Communicate(request.text, 'zh-CN-XiaoyiNeural')
    async def audio_generator():
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(audio_generator(), media_type="audio/mp3")


voiceMap = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunxia": "zh-CN-YunxiaNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

@app.get("/voice/{voiceId}")
def getVoiceById(voiceId:str):
    return ApiResult(data=voiceMap.get(voiceId))


@app.get("/voices")
def getVoiceList():
    new_list = [] 
    for key, val in voiceMap.items(): 
        new_list.append({ "name": key, "value": val}) 
    return ApiResult(data=new_list)