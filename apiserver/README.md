# Langchain开发文档
# 安装依赖
* 运行环境: python 3.12.2 , conda
* 开发环境: langchain v0.1.11 , openai v0.28.1

# pip & setuptools 更新到最新版本
```sh
python -m pip install -U pip setuptools
```


# apiserver.py 
```sh
pip install -r .\requirements.txt
uvicorn apiserver:app --reload
```


# pyaudio on mac(M1)
```sh
arch -arm64 brew install portaudio

arch -arm64 pip install --no-cache-dir --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio==0.2.11
```






# python-libmagic -> libmagic
不同操作系统需要安装不同的依赖库
## 安装 libmagic:
### mac:
```sh
brew install libmagic
```
### linux:
```sh
apt-get install libmagic1 libmagic-dev -y
```
### windows:
1. VC++ build tools
2. Win10 SDK

#### Readme
Install Microsoft Visual Studio 2022 (or later).

Install the Python development workload and the optional Python native development tools option.

Install the latest Windows SDK (under Native development in the installer).

Optional: Set $env:PlatformToolset to your toolset version before building, if it doesn't detect it.

Update to the latest setuptools Python package version.