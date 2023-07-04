# Import necessary modules
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
# load all environment variables
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env


index_name = "actest-062023"
embeddings = OpenAIEmbeddings(openai_api_key='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')
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
