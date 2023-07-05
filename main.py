# Import necessary modules
import utils

from dotenv import load_dotenv
# Import necessary libraries
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# load all environment variables
load_dotenv()


# Usage
if __name__ == "__main__":
    data_folder = Path('./ref_data/')  # Replace with your data folder path
    chunk_size = 1000  # Define the size of your text chunks here
    overlap = 50  # Define the overlap between chunks here
    use_case = "new_index"  # "existing_index" vs "new index"

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


llm = ChatOpenAI()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=chain.as_retriever(),
)

query = "How should I report the numbers of individuals in the study?"
result = qa.run(query)

print(result)
