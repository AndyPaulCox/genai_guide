# Import necessary modules
import utils
import pickle
import os
import openai
from dotenv import load_dotenv
# Import necessary libraries
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain import PromptTemplate

os.environ["TOKENIZERS_PARALLELISM"] = "true"

# load all environment variables
load_dotenv()

# Usage
if __name__ == "__main__":
    data_folder = Path('./ref_data/')  # Replace with your data folder path
    chunk_size = 1000  # Define the size of your text chunks here
    overlap = 50  # Define the overlap between chunks here
    use_case = "existing_index"  # "existing_index" vs "new index"

if use_case == "new_index":
    # This function reads in pdf or word files from the input directory and converts them into
    # chunked text that can be worked on by the AI
    text_list = utils.read_and_chunk_files_in_folder_json(data_folder, chunk_size, overlap)
    # This function reads each chunk of text at a time and summarizes into bullets and add
    # to an output dataframe bullet by bullet, the output is alist of jkey poiints from the guidlines
    sum_text_list = utils.data_prep(text_list)

    # Load the text data into Pinecone vector database for future reference
    chain = utils.text2_vec_database(sum_text_list)

    with open('doc_embedding.pickle', 'wb') as pkl:
        pickle.dump(chain, pkl)

##########################################
with open('doc_embedding.pickle', 'rb') as pkl:
    chain = pickle.load(pkl)

target_doc = utils.read_input_doc()

llm = ChatOpenAI()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=chain.as_retriever(),
)

query = f"You are an expert epidemiologist. Using your context specific knowledge of the STROBE Guidelines, please discuss what elements of the guidleines are missing or require better explantion from the following completed protocol document: {target_doc}"

response = qa.run(query)

print(response)

# specify the complete path
path = "./out_data/comments.txt"
# open file in write mode
with open(path, 'w') as file:
    file.write(response)

