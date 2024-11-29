import streamlit as st
from typing import List, Dict
from config import Config
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import HumanMessage

class ChatManager:
    def __init__(self, vectorstore=None):
        self.llm = ChatOpenAI(
            model_name=Config.OPENAI_MODEL, 
            temperature=0.3
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        self.vectorstore = vectorstore
        self.conversation_chain = None

    def initialize_conversation_chain(self):
        if self.vectorstore:
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(),
                memory=self.memory
            )

    def generate_response(self, user_input: str) -> str:
        if not self.conversation_chain:
            return "Conversation chain not initialized. Please upload and process a document first."

        try:
            # Directly get the full response
            response = self.conversation_chain({"question": user_input})
            return response["answer"]
        except Exception as e:
            return f"An error occurred: {str(e)}"



    @staticmethod
    def add_message_to_history(role: str, content: str):
        """Add a message to the chat history."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append({
            "role": role,
            "content": content
        })


    @staticmethod
    def clear_chat_history():
        """Clear the chat history and refresh the state."""
        if "messages" in st.session_state:
            st.session_state.messages = []  # Clear the chat history

    @staticmethod
    def export_chat_history():
        """Export chat history as a text file."""
        if "messages" not in st.session_state or not st.session_state.messages:
            return "No chat history available."
        
        export_content = ""
        for message in st.session_state.messages:
            role = message["role"].capitalize()
            content = message["content"]
            export_content += f"{role}: {content}\n\n"
        return export_content

    @staticmethod
    def generate_follow_up_questions(user_query: str, bot_response: str) -> List[str]:
        """
        Generate logical next questions based on user query and bot response.
        """
        llm = ChatOpenAI(
            model_name=Config.OPENAI_MODEL,
            temperature=0.3
        )

        # Properly format the prompt
        prompt = [
            HumanMessage(
                content=f"""
                Based on the conversation below, suggest 3 logical follow-up questions:

                User: {user_query}
                Bot: {bot_response}

                Follow-up questions:
                """
                # Removing the numbered format
            )
        ]

        # Generate the response
        try:
            response = llm(messages=prompt)  # Directly pass the formatted prompt to the model
            suggestions = response.content.strip().split("\n")
            
            # Filter and clean suggestions, removing any leading numbers or dots
            return [
                q.strip().replace('1.', '').replace('2.', '').replace('3.', '').strip() 
                for q in suggestions 
                if q.strip() and not q.strip().isdigit()
            ]
        except Exception as e:
            return [f"Error generating follow-up questions: {str(e)}"]
