# Import necessary modules
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
# load all environment variables
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env


index_name = PINECONE_INDEX_NAME
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINCONE_ENV)  # next to api key in console


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
