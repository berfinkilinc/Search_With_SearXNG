import os
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool
from data_flow.scraping import fetch_html, params, url
from langchain.agents import create_agent
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


load_dotenv(override=True)


openai_api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4o")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = InMemoryVectorStore(embeddings)

data = fetch_html(url)

def loading_documents(web_content):
    
    #loader = TextLoader("data-flow/content.txt", encoding = 'UTF-8')
    #documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap=200,
      add_start_index = True,
    )
    all_splits = text_splitter.split_documents(web_content)
    print(f"Split blog post into {len(all_splits)} sub-documents.")
    document_ids = vector_store.add_documents(documents=all_splits)
    return document_ids


@tool(response_format="content_and_artifact")

def retrieve_context(query: str):

    """Retrieve information to help answer a query."""
    retrieved_docs = loading_documents(data).similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retrieve_context]

prompt = (
    "You have access to a tool that retrieves context from websites. "
    "Use the tool to help answer user queries. While you answer use just this data that collected before."
)

def creating_answer(model, tools, system_prompt=prompt):  
    agent = create_agent(model, tools, system_prompt=system_prompt)

    query = (
        params['q']
    )

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()

