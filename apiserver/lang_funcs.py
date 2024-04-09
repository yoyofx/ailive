import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma,FAISS,VectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader,DirectoryLoader,BiliBiliLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT,QA_PROMPT
from langchain.schema.language_model import BaseLanguageModel
from langchain_community.embeddings import HuggingFaceEmbeddings,SentenceTransformerEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import ( PromptTemplate )
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import (ChatPromptTemplate,PromptTemplate,SystemMessagePromptTemplate,
                               AIMessagePromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder)
from langchain.memory.buffer import ConversationBufferMemory
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from typing import List
import tomllib
from typing import ( Optional)


def read_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)

def create_llm_openai(apikey:str="" ,apibase:str="",model:str="", max_tokens: Optional[int] = 1000,proxy:str="") -> BaseLanguageModel:
    '''
    Create OpenAI LLM (gpt-4-0613 / gpt-3.5-turbo)
    proxy="127.0.0.1:7890"
    '''
    if proxy != "" :
        os.environ['http_proxy'] = "socks5h://" + str 
        os.environ['https_proxy'] = "socks5h://" + str 

    os.environ['NLTK_DATA'] = os.path.join(os.path.abspath('.'), "nltk_data")
    os.environ['OPENAI_API_BASE'] =  apibase
    os.environ['OPENAI_API_KEY'] = apikey
    defaultModelName = 'gpt-3.5-turbo'
    if model != "":
        defaultModelName = model
    llm = ChatOpenAI(temperature=0, model_name = defaultModelName, max_tokens=max_tokens)
    return llm

def create_llm_agent(llm:BaseLanguageModel,prompt:str,tools:List) -> AgentExecutor: 
    memory = ConversationBufferMemory(memory_key='chat_history',
        k=10,return_messages=True)

    # tools = [note, globals()["weather"],time]

    llm_with_tools = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            ( "system", prompt ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools,memory=memory, verbose=True)
    return agent_executor

def create_knowledge_chain(llm:BaseLanguageModel,vectorstoreRetriever=None):
    '''
    基于向量存储创建知识库类型的chain, 使用方法如下:
    result =  Q({"question":"请详细讲一下这个文档主要内容是什么?"})
    print(result["answer"].strip())
    '''
    memory = ConversationBufferWindowMemory( memory_key="chat_history", k=20 ,return_messages=True)
    question_generator = LLMChain(llm=llm,prompt=CONDENSE_QUESTION_PROMPT)
    chain = load_qa_chain(llm, chain_type="stuff",prompt=QA_PROMPT)
    QA = ConversationalRetrievalChain(retriever=vectorstoreRetriever,combine_docs_chain=chain,question_generator=question_generator,memory=memory)
    return QA


def create_summarize_chain(llm:BaseLanguageModel):
    '''
    创建文档总结类型的chain, 使用方法如下:
    summ = chain({"input_documents": documents}, return_only_outputs=True)
    print(summ['output_text'])
    '''
    prompt_template = """对下面的文字,请翻译成中文:

    {text}

    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    summarizeChain = load_summarize_chain(llm, chain_type="map_reduce",return_intermediate_steps=False,combine_prompt=PROMPT)
    return summarizeChain


#!pip install bilibili-api
# brew install libmagic
# 根据文件类型,使用langchain加载文档
# such as directoryLoader('../',glob="**/*.md")
def load_docs_by_extension(file_path:str,glob="**/*"):
    isDir = os.path.isdir(file_path)
    if isDir:
        return DirectoryLoader(file_path, glob).load()
    else:
        if file_path.startswith("http"):
            return WebBaseLoader([file_path]).load()
        if file_path.endswith(".txt"):
            return TextLoader(file_path,encoding="utf-8").load()
        elif file_path.endswith(".md"):
            return TextLoader(file_path,encoding="utf-8").load()
        elif file_path.endswith(".pdf"):
            return PyMuPDFLoader(file_path).load()
        # Add more conditions for other file types
        else:
            raise ValueError("Unsupported file extension")


# Responsible for splitting the documents into several chunks
def split_docs(documents, chunk_size=1000, chunk_overlap=0):
    # Initializing the RecursiveCharacterTextSplitter with
    # chunk_size and chunk_overlap
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Splitting the documents into chunks
    chunks = text_splitter.split_documents(documents=documents)
    
    # returning the document chunks
    return chunks

def create_vectorstore(chunks:List[Document],embedding_model,name:str ,storing_path="./knowledge/"):
    vectorstore = Chroma.from_documents(chunks, embedding_model)
    vectorstore.save_local(storing_path + name)
    return vectorstore


def create_vectorstore_faiss(chunks, embedding_model, name:str, storing_path="./knowledge/"):
    USERGUIDE_INDEX = storing_path + name
    if os.path.exists(USERGUIDE_INDEX):
        print('load exists local index the embeddings using FAISS')
        #allow_dangerous_deserialization=True
        return FAISS.load_local(USERGUIDE_INDEX,embedding_model)

    print('Creating the embeddings using FAISS')
    chunks = split_docs(chunks)
    # Creating the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    # Saving the model in current directory
    vectorstore.save_local(USERGUIDE_INDEX)
    # returning the vectorstore
    return vectorstore

def load_vectorstore(store, name:str,embedding_model ,storing_path="./knowledge/"):
    USERGUIDE_INDEX = storing_path + name
    return store.load_local(USERGUIDE_INDEX,embedding_model)


def load_openai_embeddings():
    return OpenAIEmbeddings()

# function for loading the embedding model
def load_huggingface_embeddings(model_path, normalize_embedding=True):
    '''
    mkdir sentence-transformers
    cd sentence-transformers
    git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    git lfs pull
    '''
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device':'cpu'}, # here we will run the model with CPU only
        encode_kwargs = {
            'normalize_embeddings': normalize_embedding # keep True to compute cosine similarity
        }
    )


models = {
    "openai": ['gpt-4-0613', 'gpt-3.5-turbo'],
}

def getModels():
    return models

# 渠道模型
def getModelByChannel(name:str):
    return models[name]