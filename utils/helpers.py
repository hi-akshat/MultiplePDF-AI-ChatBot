import os

def is_file_size_within_limit(file, max_size_mb):
    """Check if the uploaded file is within the size limit."""
    file.seek(0, os.SEEK_END)  # Seek to the end of the file
    size_mb = file.tell() / (1024 * 1024)  # Size in MB
    file.seek(0)  # Reset file pointer to the beginning
    return size_mb <= max_size_mb

def format_message(role, content):
    """Format messages for consistent display in the chat."""
    if role == "user":
        return f"💬 {content}"
    elif role == "assistant":
        return f"🤖 {content}"
    return content
