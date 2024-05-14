import React, { FC, useEffect, useRef, useState,useImperativeHandle } from 'react'
import { OpenAIFilled } from '@ant-design/icons'
import styled from 'styled-components'
import './Footbar.css'

const Wrapper = styled.div`
border: 1px solid rgba(224, 186, 140, 0.62);
border-radius: 12px;
box-shadow: 0 6px 18px 5px rgba(191, 158, 118, 0.2);
left: 20%;
font-size: 14px;
line-height: 24px;
display: flex;
width: 60%;
height: 60px;
position: absolute;
display: flex;
justify-content: right;
align-items: center;
bottom: 50px;
background: rgba(0, 0, 0, 0.7);
opacity: 0;
transition: opacity 0.6s;
&:hover {
  opacity: 1;
}
`


export type FootbarType = {
  onEnterPress: (text: string) => void
  onRef:any
}

  const Footbar: FC<FootbarType> = (props:FootbarType) => {

    useImperativeHandle(props.onRef,()=>{
      return {
        showLoading:showLoading,
        hideLoading:hideLoading
      }
    })

    let inputReference = useRef<any>(null);
    const divReference = useRef<any>(null);
    const showLoading = () =>{
      console.log('show loading...')
      const loadingElem = document.getElementById('loading')
      if (loadingElem) {
        loadingElem.style.animationPlayState = "running"
      }
    }

    const hideLoading = ()=>{
      const loadingElem = document.getElementById('loading')
      if (loadingElem) {
        loadingElem.style.animationPlayState = "paused"
      }
    }
    

    return (
        <Wrapper id="chatbox" ref={divReference} onFocus={() => inputReference?.current?.focus()}>
          <OpenAIFilled  twoToneColor="#eb2f96" style={{cursor: 'pointer',zIndex:999,position:'absolute',marginRight:15,fontSize:25,color:'#9940ff'}}/> 
          <div id="loading" className='circle'> </div>

          <input id="input" ref={ inputReference } autoFocus style={{marginLeft:10,marginRight:50,background:'transparent',color:'azure',
              border:'none',outline:'none',width:'80%',justifyContent:'center' }}
              placeholder='请跟我聊天吧...'
              onKeyDown={(e) => {
                if (e.key === 'Escape') {
                  console.log('esc')
                  const chatbox = document.getElementById('chatbox')
                  if (chatbox) {
                    chatbox.style.opacity = '0'
                  }
                  inputReference.current.value = ''
                } else if (e.key === 'Enter') {
                  props.onEnterPress(inputReference.current.value)
                  inputReference.current.value = ''
                }
              }}
              onBlur={() => {
                inputReference?.current?.focus()
              }}
              ></input>
        </Wrapper> 
      )
  }

  export default Footbar
