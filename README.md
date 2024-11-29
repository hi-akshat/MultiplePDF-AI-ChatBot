# MultiplePDF-AI-Chatbot

# Chat with Documents and Websites

This is a Streamlit-powered web application that allows users to chat with content from uploaded PDFs and websites. The app leverages LangChain, OpenAI APIs, and vector databases to provide meaningful, context-aware responses. Additionally, it suggests follow-up questions dynamically to enhance user interaction.

---

## **Features**

- **PDF Document Support**:
  - Upload multiple PDF files.
  - Extract and process text from PDFs.
  - Create vector embeddings for efficient document retrieval.
  
- **Website Content Support**:
  - Input a URL to include the content of a website as part of the knowledge base.
  - Automatically process and integrate web content into the conversation.

- **Interactive Chat**:
  - Engage in real-time conversations with the knowledge base.
  - Ask questions about the documents and websites you uploaded.
  - Get dynamic, logical follow-up question suggestions after each response.

- **Export Chat History**:
  - Download the chat history as a `.txt` file.

- **Enhanced User Experience**:
  - Typing speed effect for bot responses.
  - Right-sidebar support for a sleek and modern layout.

---

## **Technologies Used**

- **Frontend**:
  - [Streamlit](https://streamlit.io/) for building the interactive web application.
  - Custom CSS for enhanced UI and styling.

- **Backend**:
  - [LangChain](https://www.langchain.com/) for conversational AI and retrieval-based question answering.
  - [OpenAI API](https://openai.com/api/) for generating responses and follow-up questions.

- **Vector Storage**:
  - [FAISS](https://faiss.ai/) for vector-based retrieval of content.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/chat-with-documents-and-websites.git
   cd chat-with-documents-and-websites
