# Import necessary libraries
import os
from PyPDF2 import PdfReader
from docx import Document
from datetime import date
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Function to read and chunk the contents of PDF and DOCX files in a folder
def read_and_chunk_files_in_folder(f_folder_path, f_chunk_size, f_overlap):
    # Initialize a RecursiveCharacterTextSplitter object with the chunk size and overlap specified
    splitter = RecursiveCharacterTextSplitter(f_chunk_size, f_overlap)

    # Empty list to store data
    data = []

    # Loop through each file in the directory specified by f_folder_path
    for filename in os.listdir(f_folder_path):
        # Check if the file ends with ".pdf"
        if filename.endswith(".pdf"):
            # Read the content of the PDF file
            text = PdfReader(os.path.join(f_folder_path, filename))
        # Else check if the file ends with ".docx"
        elif filename.endswith(".docx"):
            # Read the content of the DOCX file
            text = Document(os.path.join(f_folder_path, filename))
        # If the file is neither PDF nor DOCX, skip to the next file
        else:
            continue

        # Split the text into chunks
        chunks = splitter.split_documents(text)

        # For each chunk, create a dictionary with file name, current date, and the text chunk
        # Append this dictionary to the data list
        for chunk in chunks:
            data.append({'filename': filename,
                         'date': date.today().strftime("%Y-%m-%d"),
                         'text_chunk': chunk})

    # Convert the data list into a pandas DataFrame and return it
    return pd.DataFrame(data)
