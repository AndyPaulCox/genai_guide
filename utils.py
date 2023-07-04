# Import necessary libraries
import os
import openai
import tiktoken
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader

# Embeddings

# Function to read and chunk the contents of PDF and DOCX files in a folder


# Using a JSON file instead of Pandas DF
def read_and_chunk_files_in_folder_json(f_folder_path, f_chunk_size, f_overlap):
    documents = []
    for file in os.listdir(f_folder_path):
        if file.endswith('.pdf'):
            pdf_path = './ref_data/' + file
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        elif file.endswith('.docx') or file.endswith('.doc'):
            doc_path = './ref_data/' + file
            loader = Docx2txtLoader(doc_path)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            text_path = './ref_data/' + file
            loader = TextLoader(text_path)
            documents.extend(loader.load())

    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=f_chunk_size, chunk_overlap=f_overlap)
    chunks = text_splitter.split_documents(documents)

    # For each chunk, create a dictionary with file name, current date, and the text chunk
    page_content_chunk = []
    for chunk in chunks:
        page_content_chunk.append(chunk.page_content)

    # Loop through each index and clean the chunk and replace into the list
    for i, chunk in enumerate(page_content_chunk):
        # Clean the chunk and replace it in the list
        page_content_chunk[i] = clean_text(chunk)

    # Convert the documents list into a JSON object and return it

    return page_content_chunk


# The summarise_text function takes a string of text as input, uses the OpenAI
# API to generate a summary of the text using the ChatGPT 3.5 model, and returns the summary.
# The data_prep function cleans and summarises the text chunks in the DataFrame.
# It loops through each row in the DataFrame, cleans the text chunk, and skips the
# iteration if the cleaned text is empty. It then summarises the cleaned text, splits the
# summary into statements, and appends each statement along with the corresponding filename
# and date to the data list. This list is then converted into a pandas DataFrame.
# You might need to adjust the temperature and max_tokens parameters based on your specific needs.
# The temperature parameter controls the randomness of the generated text (higher values make the
# text more random), while the max_tokens parameter controls the maximum length of the generated summary.
# Again, please note that usage of GPT-3 involves cost, and you'll need API credentials from OpenAI
# to access their models. You should also handle exceptions and add error checks as necessary
# Function to summarise the text


def summarise_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the ChatGPT 3.5
        prompt=(f"You are an expert epidemiologist. Please summarize the following text in "
                f"bullet points and add a fullstop at the end of each bullet:\n{text}\n\nSummary:"),
        # Higher value (close to 1) means more randomness, lower value (close to 0) means more determinism
        temperature=0.3,
        max_tokens=100  # Maximum length of the generated summary
    )
    return response.choices[0].text.strip()


# Function to prepare the data
def data_prep(df):
    # Initialize an empty list to store the data
    data = []
    # Loop through each row in the DataFrame
    for chunk in df:
        # Clean the text chunk
        text = clean_text(chunk)
        # Skip this iteration if the cleaned text is empty
        if not text:
            continue
        # Summarise the text chunk
        summary = summarise_text(text)
        # Split the summary into statements
        statements = summary.split('. ')
        # Loop through each statement
        # Append a dictionary with the filename, date, and statement to the data list
        for state in statements:
            data.append(state)
    # Convert the data list into a pandas DataFrame and return it
    return data


def clean_text(text):
    # Decode the text using UTF-8 encoding and ignore non-UTF-8 characters
    text = text.encode("utf-8", errors="ignore").decode("utf-8")

    # Trim leading and trailing whitespace
    text = text.strip()

    # Replace multiple spaces with a single space
    text = " ".join(text.split())

    return text


def text2_vec_database(text):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPEANAI_API_KEY"))
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV")  # next to api key in console
    )

    # Backend / langchain
    index = Pinecone.from_texts(texts=text, index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embeddings)

    return index
