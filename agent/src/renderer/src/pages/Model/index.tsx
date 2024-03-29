import React, { useEffect, useLayoutEffect, useRef, useState } from 'react'
import styled from 'styled-components'

import { debounce } from '@src/renderer/src/utils'
import LegacyRender from './Legacy'
import CurrentRender from './Current'
import Toolbar from './Toolbar'
import Tips, { TipsType } from './Tips'
import Footbar from './Footbar'
import { useDispatch, useSelector } from 'react-redux'
import zhTips from './tips/zh.json'
import enTips from './tips/en.json'
import { Dispatch, RootState } from '../../store'
import  WebSocketComponent from './WebSocket'

//'ws://localhost:8000/ws'
interface ITips {
  mouseover: Mouseover[]
  click: Mouseover[]
}

interface Season {
  date: string
  text: string
}

interface Mouseover {
  selector: string
  text: string[]
}

const Wrapper = styled.div<{ border: boolean }>`
  ${(props) => (props.border ? 'border: 2px dashed #ccc;' : 'padding: 2px;')}
  height: 100vh;
  width: 100vw;
  overflow: hidden;
`

const RenderWrapper = styled.div`
  margin-top: 20px;
`

const getCavSize = () => {
  return {
    width: window.innerWidth,
    height: window.innerHeight - 20,
  }
}

const Model = () => {
  const { modelPath: originModelPath, resizable,  useGhProxy, language,showTool } = useSelector((state: RootState) => ({ ...state.config, ...state.win, }))

  const modelPath =
    useGhProxy && originModelPath.startsWith('http') ? `https://mirror.ghproxy.com/${originModelPath}` : originModelPath

  const dispatch = useDispatch<Dispatch>()

  const [tips, setTips] = useState<TipsType>({ text: '', priority: -1,  timeout: 0 })

  const [cavSize, setCavSize] =
    useState<{ width: number; height: number }>(getCavSize)

  useEffect(() => {
    ;(window as any).setSwitchTool = dispatch.win.setSwitchTool
    ;(window as any).setLanguage = dispatch.win.setLanguage
    ;(window as any).nextModel = dispatch.config.nextModel
    ;(window as any).prevModel = dispatch.config.prevModel
  }, [])

  useEffect(() => {
    const handleDragOver = (evt: DragEvent): void => {
      evt.preventDefault()
    }
    const handleDrop = async (evt: DragEvent) => {
      evt.preventDefault()

      const files = evt.dataTransfer?.files

      if (!files) {
        return
      }

      const paths = []
      for (let i = 0; i < files.length; i++) {
        const result = await window.bridge.getModels(files[i])
        paths.push(...result)
      }

      console.log('modelList: ', paths)

      if (paths.length > 0) {
        const models = paths.map((p) => `file://${p}`)

        dispatch.config.setModelList(models)
        dispatch.config.setModelPath(models[0])
      }
    }

    document.body.addEventListener('dragover', handleDragOver)
    document.body.addEventListener('drop', handleDrop)

    return () => {
      document.body.removeEventListener('dragover', handleDragOver)
      document.body.removeEventListener('drop', handleDrop)
    }
  }, [])

  useLayoutEffect(() => {
    const resizeCanvas = debounce(() => {
      setCavSize(getCavSize())
    })

    window.addEventListener('resize', resizeCanvas, false)

    return () => {
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [])

  useEffect(() => {
    const handleBlur = () => {
      if (resizable) {
        dispatch.win.setResizable(false)
      }
    }


    window.addEventListener('blur', handleBlur)
    return () => {
      window.removeEventListener('blur', handleBlur)
    }
  }, [])

  const isMoc3 = modelPath.endsWith('.model3.json')

  const Render = isMoc3 ? CurrentRender : LegacyRender

  const tipJSONs = language === 'en' ? enTips : zhTips


  const handleMessageChange = (nextTips: TipsType) => {
    setTips(nextTips)
  }

  const showMessage = (text: string, timeout: number) => {
    handleMessageChange({ text: text,timeout: timeout,priority: 9999})
  }

  const handleMouseOver: React.MouseEventHandler<HTMLDivElement> = (event) => {
    const tips = tipJSONs.mouseover.find((item) =>
      (event.target as any).matches(item.selector),
    )
    if (tips){
      let text = Array.isArray(tips.text)? tips.text[Math.floor(Math.random() * tips.text.length)]: tips.text
      text = text.replace('{text}', (event.target as HTMLDivElement).innerText)
      handleMessageChange({ text, timeout: 2000, priority: 1, })
    }
  }

  const handleClick: React.MouseEventHandler<HTMLDivElement> = (event) => {
    const tips = tipJSONs.click.find((item) =>
      (event.target as any).matches(item.selector),
    )
    if (tips){
      let text = Array.isArray(tips.text)? tips.text[Math.floor(Math.random() * tips.text.length)]: tips.text
      text = text.replace('{text}', (event.target as HTMLDivElement).innerText)
      handleMessageChange({ text, timeout: 2000, priority: 1, })
    }
  }

  const doubleClick: React.MouseEventHandler<HTMLDivElement> = (event) => {
    let text: string = "hello"
    handleMessageChange({ text, timeout: 2000,  priority: 1})
  }



  const [ws,setWS] = useState<WebSocket>()
  const synth = window.speechSynthesis;


  const onChat = (text: string) => {
    ws?.send(text)
  }

  const onMessage = (text: string) => {
    showMessage(text, 5000)

    const voice = synth.getVoices()[0]
    console.log(voice)
    const utterThis = new SpeechSynthesisUtterance(text)
    utterThis.pitch = 1.4
    utterThis.rate = 0.8
    utterThis.lang= 'zh-cn'
    //utterThis.voice = voice
    synth.speak(utterThis)
  }

  // window.speechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
  // const recognition = new window.speechRecognition()
  // recognition.interimResults = true;
  // recognition.maxAlternatives = 10;
  // recognition.continuous = true;
  // let finalTranscript = "";

  // recognition.onresult = event => {
  //   let interimTranscript = "";
  //   for (
  //     let i = event.resultIndex, len = event.results.length;
  //     i < len;
  //     i++
  //   ) {
  //     let transcript = event.results[i][0].transcript;
  //     if (event.results[i].isFinal) {
  //       finalTranscript += transcript;
  //     } else {
  //       interimTranscript += transcript;
  //     }
  //   }
  
  //   console.log(finalTranscript + interimTranscript)
  // };
  

  return (
    <Wrapper
      border={resizable}
      onMouseOver={isMoc3 ? undefined : handleMouseOver}
      onClick={isMoc3 ? undefined : handleClick}
      onDoubleClick={doubleClick}
    >
      <Tips {...tips}></Tips>
      {showTool && <Toolbar onShowMessage={handleMessageChange}></Toolbar>}
      <RenderWrapper>
        <Render {...cavSize} modelPath={modelPath}></Render>
      </RenderWrapper>
      
      <WebSocketComponent url='ws://localhost:8000/ws' onMessage={onMessage} setWS={setWS}></WebSocketComponent>
      <Footbar onEnterPress={onChat}></Footbar>
    </Wrapper>
  )
}

export default Model
