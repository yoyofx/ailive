import React, { FC, useEffect, useRef, useState } from 'react'
import styled from 'styled-components'

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
}

  const Footbar: FC<FootbarType> = (props:FootbarType) => {
    let inputReference = useRef(null);
    const divReference = useRef(null);

    return (
        <Wrapper id="chatbox" ref={divReference} onFocus={() => inputReference?.current?.focus()}>
          <input id="input" ref={ inputReference } autoFocus style={{margin:8,background:'transparent',color:'azure',
              border:'none',outline:'none',width:'80%',justifyContent:'center' }}
              placeholder='请跟我聊天吧...'
              onKeyDown={(e) => {
                if (e.key === 'Escape') {
                  console.log('esc')
                  const chatbox = document.getElementById('chatbox')
                  chatbox.style.opacity = '0'
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
