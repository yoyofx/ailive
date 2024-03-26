from lang_funcs import (load_docs_by_extension,split_docs,
        create_vectorstore_faiss,create_vectorstore,
        load_openai_embeddings,load_huggingface_embeddings,
        create_knowledge_chain,create_summarize_chain,create_llm_openai
)

from typing import Union
from fastapi import FastAPI,WebSocket
from fastapi.responses import HTMLResponse

import os

chat = create_llm_openai( apikey='fk224285-rmfTvLRKQyarQdyF5YBX6IlfKVKTj1y1',
                         apibase='https://openai.api2d.net/v1')

embeddings = load_huggingface_embeddings('all-MiniLM-L6-v2')

doc_url = "https://maomi.whuanle.cn/"

documents = load_docs_by_extension(doc_url)

#documents = load_docs_by_extension("README.md")

print (f'There are {len(documents)} document(s) in this document.')
print (f'There are {len(documents[0].page_content)} characters in the first page of your document.')
 
#vectorstore = create_vectorstore(documents,embeddings)
vectorstore = create_vectorstore_faiss(documents,embeddings,"readme")

Q = create_knowledge_chain(chat,vectorstore.as_retriever())

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
        result = Q({"question": data })["answer"].strip()
        await websocket.send_text(f"AI: {result}")