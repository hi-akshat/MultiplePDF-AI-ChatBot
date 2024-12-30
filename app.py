#test comment for git functionality
import streamlit as st
from config import Config
from components.chat_logic import ChatManager
from components.pdf_processor import PDFProcessor
import time

def load_css(file_path):
    """Load CSS styles."""
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def reset_session():
    """Reset all session variables and clear the chat history."""
    st.session_state.processed_files = []
    st.session_state.messages = []
    st.session_state.suggested_questions = []
    if "chat_manager" in st.session_state:
        del st.session_state["chat_manager"]
    if "vectorstore" in st.session_state:
        del st.session_state["vectorstore"]

def add_footer():
    """Add a footer with creator attribution and LinkedIn link."""
    footer_html = """
    <div class="footer">
        <p>Created by 
                Akshat Gupta with ❤️ @UC Berkeley | 
            <a href="https://www.linkedin.com/in/iamakshat/" target="_blank">
                LinkedIn
            </a>
            |
            <a href="mailto:akshat.g@berkeley.edu">
                Email
            </a>
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def main():
    # Set up the page configuration
    st.set_page_config(page_title=Config.APP_TITLE, layout="wide")

    # Initialize session state for processed files
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []

    # Load styles dynamically
    load_css("styles/main.css")

    # Initialize PDF processing
    pdf_processor = PDFProcessor()

    # Sidebar: PDF Upload
    st.sidebar.header("📤 Upload Documents")
    pdf_docs = st.sidebar.file_uploader(
        "Upload PDFs",
        type=Config.SUPPORTED_FILE_TYPES,
        accept_multiple_files=True,
    )

    # Display list of processed documents
    if st.session_state.processed_files:
        st.sidebar.write("Processed Documents:")
        for file in st.session_state.processed_files:
            st.sidebar.markdown(f"📄 {file.name}")
    else:
        st.sidebar.write("No documents processed yet.")

    # Process Documents Button
    process_button_clicked = st.sidebar.button("Process Documents")

    if process_button_clicked:
        with st.spinner("🔍 Analyzing documents..."):
            if pdf_docs:
                raw_text = pdf_processor.extract_text(pdf_docs)
                text_chunks = pdf_processor.split_text(raw_text)
                vectorstore = pdf_processor.create_vectorstore(text_chunks)

                if vectorstore:
                    chat_manager = ChatManager(vectorstore=vectorstore)
                    chat_manager.initialize_conversation_chain()
                    st.session_state["chat_manager"] = chat_manager
                    st.session_state.processed_files.extend(pdf_docs)
                    st.sidebar.success("✨ Documents processed successfully!")
                else:
                    st.sidebar.error("Document processing failed.")
            else:
                st.sidebar.warning("No documents uploaded to process.")

    # Export Functionality
    if st.sidebar.button("Export Chat"):
        if "messages" in st.session_state and st.session_state.messages:
            chat_history = ChatManager.export_chat_history()
            st.sidebar.download_button(
                label="Download Chat History",
                data=chat_history,
                file_name="chat_history.txt",
                mime="text/plain"
            )
        else:
            st.sidebar.warning("No chat history available to export.")

    # Main App Title
    st.title(Config.APP_TITLE)

    # Initialize session state for chat and suggestions
    if "suggested_questions" not in st.session_state:
        st.session_state.suggested_questions = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Suggested Questions Container
    suggested_container = st.container()

    # Prepare user input
    user_input = None

    # Display Suggested Questions in a way that doesn't interfere with chat input
    if st.session_state.suggested_questions:
        with suggested_container:
            st.write("💡 Suggested Follow-up Questions:")
            # Use columns to spread out buttons and prevent layout issues
            cols = st.columns(len(st.session_state.suggested_questions))
            for i, question in enumerate(st.session_state.suggested_questions):
                with cols[i]:
                    if st.button(question, key=f"suggested_{i}"):
                        user_input = question
                        break

    # Ensure text input is always visible AFTER suggested questions
    if "chat_manager" in st.session_state and st.session_state["chat_manager"].conversation_chain:
        user_input = user_input or st.chat_input("Ask a question about your documents")
    else:
        st.warning("🚨 Please upload and process PDF documents before asking questions.")
        st.chat_input("Ask a question about your documents", disabled=True)

    # Process user input
    if user_input:
        if "chat_manager" not in st.session_state or not st.session_state["chat_manager"].conversation_chain:
            st.warning("🚨 Please upload and process PDF documents before asking questions.")
        else:
            chat_manager = st.session_state["chat_manager"]

            # Add and display user message
            ChatManager.add_message_to_history("user", user_input)
            with st.chat_message("user"):
                st.markdown(user_input)

            # Generate and display assistant response with streaming
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Generate the full response
                full_response = chat_manager.generate_response(user_input)
                
                # Stream the response character by character
                for i in range(1, len(full_response) + 1):
                    response_placeholder.markdown(full_response[:i] + "▌")
                    time.sleep(0.01)  # Adjust the speed of typing
                
                # Final display of the complete response
                response_placeholder.markdown(full_response)
                
                ChatManager.add_message_to_history("assistant", full_response)

            # Generate new follow-up questions immediately after bot response
            st.session_state.suggested_questions = ChatManager.generate_follow_up_questions(user_input, full_response)

            # Rerun to refresh the page and show new suggested questions
            st.rerun()

    # Clear Chat History Button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.suggested_questions = []
        st.session_state.processed_files = []
        st.rerun()

    if st.sidebar.button("Reset Session", type="primary"):
        reset_session()
        st.sidebar.success("Session reset successfully!")
        st.rerun()

    add_footer()


if __name__ == "__main__":
    main()