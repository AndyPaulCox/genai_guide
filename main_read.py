# Import necessary modules
import utils
import os
from dotenv import load_dotenv
# Import necessary libraries
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
# load all environment variables
load_dotenv()

# Usage
if __name__ == "__main__":
    data_folder = Path('./ref_data/')  # Replace with your data folder path
    chunk_size = 1000  # Define the size of your text chunks here
    overlap = 50  # Define the overlap between chunks here
    use_case = "existing_index"  # "existing_index" vs "new index"

if use_case == "new index":
    # This function reads in pdf or word files from the input directory and converts them into
    # chunked text that can be worked on by the AI
    text_list = utils.read_and_chunk_files_in_folder_json(data_folder, chunk_size, overlap)
    # This function reads each chunk of text at a time and summarizes into bullets and add
    # to an output dataframe bullet by bullet, the output is alist of jkey poiints from the guidlines
    sum_text_list = utils.data_prep(text_list)

    # Load the text data into Pinecone vector database for future reference
    chain = utils.text2_vec_database(sum_text_list)

##########################################
index_name = "actest-062023"
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# initialize pinecone
pinecone.init(
    api_key='9eeb3e8e-de52-45f6-9ef4-52ebd88737ab',  # find at app.pinecone.io
    environment='asia-southeast1-gcp-free')  # next to api key in console

doc_db = Pinecone.from_existing_index(index_name, embeddings)

llm = ChatOpenAI()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=doc_db.as_retriever(),
)

query = "How should I report the numbers of individuals in the study?"
result = qa.run(query)

print(result)
