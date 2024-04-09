from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.schema.language_model import BaseLanguageModel
from lang_funcs import ( create_llm_openai,create_llm_agent,read_toml,getModels,getModelByChannel )
from init import (initialization)
from lang_tools import *

from typing import Union
from fastapi import FastAPI,WebSocket
from fastapi.responses import StreamingResponse,JSONResponse
import edge_tts as tts
from pydantic import BaseModel

agent_executor = initialization("./config.toml")
 
app = FastAPI()


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

@app.get("/models/{channel}")
async def getModels(channel:Union[str,None]=None):
    if not channel:
        return ApiResult(data=getModels())
    else :
        return ApiResult(data=getModelByChannel(channel))



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