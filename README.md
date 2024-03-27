## Readme
目前后端使用api2d代理gpt3.5服务.


## 项目结构
* agent: 智能代理,基于 electron 的桌面客户端,跨平台兼容 Windows / MacOS.

* apiserver: 基本python/fastapi/langchain 构建的后端应用,用于驱动chat/知识库/语音识别/text to voice 等场景的服务.

# 规划:
1. 可维护的多模型: openai/gemini/ollama(本地) 等.
2. 桌面端支持语音识别和语音对话
3. 聊天窗口
4. 知识库
5. Agent 识别的语言或文本 执行命令os



# 目前规则: v0.1 版本
产品形态: 老婆是一个使用live2d技术显示在桌面,她/他可以由用户定制, 性格 称呼 和一些特定的聊天回复

## 设定:
老婆 =  大模型/ 人物(显示) / 人物设定 / 知识库
