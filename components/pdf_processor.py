import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st

class PDFProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()

    def extract_text(self, pdf_docs):
        """Extract text from multiple PDF documents."""
        text = ""
        if not pdf_docs:
            st.warning("No PDF files uploaded.")
            return text

        for pdf in pdf_docs:
            try:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception as e:
                st.error(f"Failed to read {pdf.name}: {str(e)}")
        return text

    def split_text(self, raw_text):
        """Split extracted text into chunks."""
        text_splitter = CharacterTextSplitter(
            separator="\n", 
            chunk_size=1000, 
            chunk_overlap=200, 
            length_function=len
        )
        chunks = text_splitter.split_text(raw_text)
        print("Number of text chunks:", len(chunks))  # Debug
        return chunks

    def create_vectorstore(self, text_chunks):
        """Create a FAISS vectorstore from text chunks."""
        if not text_chunks:
            st.error("No text chunks available to create a vectorstore.")
            return None

        try:
            vectorstore = FAISS.from_texts(texts=text_chunks, embedding=self.embeddings)
            print("Vectorstore created successfully.")  # Debug
            return vectorstore
        except Exception as e:
            st.error(f"Failed to create vectorstore: {str(e)}")
            return None
