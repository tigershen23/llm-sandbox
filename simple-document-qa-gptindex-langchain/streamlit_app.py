# For now, it's a manual process of updating this file when we make changes to document_qa.ipynb

from gpt_index import GPTListIndex, SimpleWebPageReader, BeautifulSoupWebReader, GPTSimpleVectorIndex
from IPython.display import Markdown, display
from langchain.agents import load_tools, Tool, initialize_agent, ZeroShotAgent, AgentExecutor
from langchain.llms import OpenAI
from langchain import OpenAI, LLMChain
from pathlib import Path
import hashlib
import streamlit as st 

# Set up document QA index
def get_document_index():
    Input_URL = "https://experiencewelcome.zendesk.com/hc/en-us/articles/12461508447124-Hubspot-Integration-Documentation"
    hashed_input_url = hashlib.md5(Input_URL.encode("ascii")).hexdigest()
    index_filepath = f"./doc_qa_{hashed_input_url}.json"
    try:
        index = GPTSimpleVectorIndex.load_from_disk(index_filepath)
    except FileNotFoundError:
        documents = SimpleWebPageReader(html_to_text=True).load_data([Input_URL])
        tmp_index = GPTSimpleVectorIndex(documents)
        tmp_index.save_to_disk(index_filepath)
        index = GPTSimpleVectorIndex.load_from_disk(index_filepath)

    return index

# Query DB
def querying_db(query: str):
    response = get_document_index().query(query, verbose=True)
    return response

# Create LangChain agent
def get_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=querying_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent

# Streamlit interface
def main():
    st.title("Welcome Docs QA")

    search = st.container()
    query = search.text_input('Ask a question about the Welcome docs!', '', placeholder='Ex: Which CRMs does Welcome integrate with?')

    if search.button("Go!") or query != "":
        with st.spinner("Retrieving, give me a bit..."):
            # ask the question
            agent = get_agent()
            answer = agent.run(query)
        # display the answer
        st.write(answer)

if __name__ == "__main__":
    main()