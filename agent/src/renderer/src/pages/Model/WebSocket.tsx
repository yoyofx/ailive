import React, { FC, useEffect, useRef, useState } from 'react'


export type WebSocketType = {
    url:string
    onMessage: (message: string) => void
    setWS:any

}

const WebSocketComponent: FC<WebSocketType> = (props) => { 

    const createWebSocket = (url:string) => {
        //const url = 'ws://localhost:8000/ws'
        try {
          let ws1 = new WebSocket(url)
          props.setWS(ws1)
          initWebsocket(ws1,url)
        } catch (error) {
          console.log(error);
          reconnect(url);
        }
      }
    
      const initWebsocket = (ws:WebSocket,wsUrl:string) => {
        ws.onclose = function () {
            console.log('链接关闭');
            reconnect(wsUrl);
          };
          ws.onerror = function() {
            console.log('发生异常了');
            reconnect(wsUrl);
          };
          ws.onopen = function () {
            console.log('connected');
          };
          ws.onmessage = function (event) {
            console.log('received: %s', event.data)
            //showMessage(event.data, 2000)
            props.onMessage(event.data)
          }
      }
    
      var lockReconnect = false;//避免重复连接
    
      const reconnect = (wsUrl:string) => {
        if(lockReconnect) {
          return;
          };
          lockReconnect = true;
          //没连接上会一直重连，设置延迟避免请求过多
          let tt 
          clearTimeout(tt);
          tt = setTimeout(function () {
          createWebSocket(wsUrl);
          lockReconnect = false;
          }, 2000);
      }
    
      useEffect(() => {
        createWebSocket(props.url)
      },[])

    return <></>
}


export default WebSocketComponent