import os
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma,FAISS,VectorStore
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT,QA_PROMPT
from IPython.display import Markdown, display
from datetime import date
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.chains.summarize import load_summarize_chain
from lang_funcs import (load_docs_by_extension,split_docs,
        create_vectorstore_faiss,create_vectorstore,
        load_openai_embeddings,load_huggingface_embeddings,
        create_knowledge_chain,create_summarize_chain,create_llm_openai
)



# chat = create_llm_openai()
embeddings = load_huggingface_embeddings('all-MiniLM-L6-v2')

doc_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023"

docs = load_docs_by_extension(doc_url)

# #docs = load_docs_by_extension('./README.md')

# print (f'There are {len(docs)} document(s) in this document.')
# print(docs)
# print (f'There are {len(docs[0].page_content)} characters in the first page of your document.')
 
# documents = split_docs(docs)



print('load modit')
query_result = embeddings.embed_query(docs)
print(query_result)