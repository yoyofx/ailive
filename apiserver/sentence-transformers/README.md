# 下载模型
## 方法1：Git Large File Storage
https://git-lfs.com/

### Homebrew install
```sh
brew install git-lfs
```

```sh
git lfs install
```
### git clone 模型
```sh
mkdir sentence-transformers
cd sentence-transformers
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
git lfs pull
```


## 方法2：支持断点续传和进度显示，解决网络问题
```sh
git clone https://github.com/git-cloner/aliendao
cd aliendao
pip install -r requirements.txt

python .\model_download.py --repo_id sentence-transformers/all-MiniLM-L6-v2
```
