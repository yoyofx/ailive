## Readme
目前后端使用api2d代理gpt3.5服务.


## 项目结构
* agent: 智能代理,基于 electron 的桌面客户端,跨平台兼容 Windows / MacOS.

* apiserver: 基本python/fastapi/langchain 构建的后端应用,用于驱动chat/知识库/语音识别/text to voice 等场景的服务.

# 规划:
1. 可维护的多模型: openai/gemini/ollama(本地) 等.
2. 