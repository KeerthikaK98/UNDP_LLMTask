import streamlit as st
import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from config import ffd4_URL, index_path, doc_path, embedding_model_, llm_model, persist_dir

st.title("Climate Finance Document Explorer")

# Loading components

@st.cache_resource
def load_chain():
    embedding_model = HuggingFaceEmbeddings(model_name = embedding_model_)
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
    llm_ = Ollama(model = llm_model)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_, retriever=vectordb.as_retriever(search_type="similarity", search_kwargs={"k":2}),
        return_source_documents=True,
        chain_type="stuff"
)
    return qa_chain



# UI 
query = st.text_input("Ask a question")
if query:
    chain = load_chain()
    if chain is None:
        st.stop()
        
    with st.spinner("Thinking..."):
        chain = load_chain()
        response = chain.invoke(query)
        st.subheader("Answer")
        st.write(response["result"])
        #st.subheader("Sources")
        #for doc in response["source_documents"]:
         #   st.markdown(f"-`{doc.metadata.get('source', 'unknown')}`")