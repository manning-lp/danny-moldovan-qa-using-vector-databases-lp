from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    """
    Extract text from an HTML file.
    
    Parameters:
    - file_path (str): Path to the HTML file.
    
    Returns:
    - Extracted text from the HTML.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract and return text from the HTML content
    return soup.get_text()


import tiktoken

def split_text_by_tokens(text, max_tokens=300):
    """
    Split text based on token count using the tiktoken library.
    
    Parameters:
    - text (str): Text to be split.
    - model_name (str): Name of the model to get the tokenizer for.
    - max_tokens (int): Maximum number of tokens per chunk.
    
    Returns:
    - List of text chunks, each not exceeding max_tokens.
    """
    
    # Get the encoder (tokenizer) for the specified model
    tokenizer = tiktoken.get_encoding('cl100k_base')
    
    # Split the text into chunks based on token count
    chunks = []
    current_chunk = ""
    for word in text.split():
        # Check if adding the word doesn't exceed the max_token count
        if len(tokenizer.encode(current_chunk + " " + word)) <= max_tokens:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
    # Append any remaining text
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

import os

def process_directory(directory, max_tokens=400):
    """
    Process all HTML files within a directory (and its subdirectories), extracting text and splitting based on token count.
    
    Parameters:
    - directory (str): The root directory to start the search for HTML files.
    - max_tokens (int): Maximum number of tokens per chunk.
    
    Returns:
    - Dictionary with file paths as keys and lists of text chunks as values.
    """
    results = {}
    
    # Loop through the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                text = extract_text_from_html(file_path)
                chunks = split_text_by_tokens(text, max_tokens)
                results[file_path] = chunks
                
                
    return results