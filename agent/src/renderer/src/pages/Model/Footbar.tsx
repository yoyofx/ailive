import React, { FC, useEffect, useRef, useState } from 'react'
import styled from 'styled-components'

const Wrapper = styled.div`
border: 1px solid rgba(224, 186, 140, 0.62);
border-radius: 12px;
box-shadow: 0 6px 25px 8px rgba(191, 158, 118, 0.2);
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

  const Footbar: FC = (props) => {
    const inputReference = useRef(null);

    return (
        <Wrapper onFocus={() => inputReference.current.focus()}>
          <input ref={inputReference} autoFocus style={{margin:8,background:'transparent',color:'azure',
              border:'none',outline:'none',width:'80%',justifyContent:'center' }}
              placeholder='请跟我聊天吧...'
              ></input>
        </Wrapper>
      )
  }

  export default Footbar
