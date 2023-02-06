# For now, it's a manual process of updating this file when we make changes to document_qa.ipynb
# MAKE SURE YOU'VE RUN THE CRAWLERS BEFORE RUNNING THIS APP OR IT WON'T WORK

from gpt_index import GPTListIndex, SimpleWebPageReader, SimpleDirectoryReader, BeautifulSoupWebReader, GPTSimpleVectorIndex
from IPython.display import Markdown, display
from langchain.agents import load_tools, Tool, initialize_agent, ZeroShotAgent, AgentExecutor
from langchain.llms import OpenAI
from langchain import OpenAI, LLMChain
from pathlib import Path
import hashlib
import streamlit as st

#region marketing site supporting code
# Set up document QA index
@st.cache(allow_output_mutation=True)
def get_marketing_site_index():
    welcome_marketing_site_data = SimpleDirectoryReader("./crawls/collections/welcome_marketing/pages").load_data()
    welcome_marketing_site_index = GPTSimpleVectorIndex(welcome_marketing_site_data)

    return welcome_marketing_site_index

# Query DB
def query_marketing_site_db(query: str):
    return get_marketing_site_index().query(query, verbose=True)

# Create LangChain agent
def get_marketing_site_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=query_marketing_site_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
#endregion

#region blog supporting code
# Set up document QA index
@st.cache(allow_output_mutation=True)
def get_blog_index():
    welcome_blog_data = SimpleDirectoryReader("./crawls/collections/welcome_marketing/pages").load_data()
    welcome_blog_index = GPTSimpleVectorIndex(welcome_blog_data)

    return welcome_blog_index

# Query DB
def query_blog_db(query: str):
    return get_blog_index().query(query, verbose=True)

# Create LangChain agent
def get_blog_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=query_blog_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
#endregion

# Streamlit interface
def main():
    # st.title("Welcome Question-Answering")

    st.header("Welcome Marketing Site Q&A")

    marketing_site_search = st.container()
    marketing_site_query = marketing_site_search.text_input(
        'Ask a question about anything public about Welcome!',
        '',
        placeholder='Ex: What are some features of Welcome that help engage an audience?'
    )

    previous_marketing_site_query = ""
    if marketing_site_search.button("Go!", key="Marketing Site Go button") or marketing_site_query != previous_marketing_site_query:
        previous_marketing_site_query = marketing_site_query
        with st.spinner("What is the difference between a hippo and a zippo? One is really heavy, the other is a little lighter..."):
            marketing_site_agent = get_marketing_site_agent()
            marketing_site_answer = marketing_site_agent.run(marketing_site_query)
        marketing_site_search.write(marketing_site_answer)

    st.write("━" * 34)

    st.header("Welcome Blog Q&A")

    blog_search = st.container()
    blog_query = blog_search.text_input(
        "Ask a question about anything written on Welcome's blog!",
        '',
        placeholder='Ex: What can you do with Agenda Builder in Welcome?'
    )

    previous_blog_query = ""
    if blog_search.button("Go!", key="Blog Go button") or blog_query != previous_blog_query:
        with st.spinner("One mississippi, two mississippi..."):
            blog_agent = get_blog_agent()
            blog_answer = blog_agent.run(blog_query)
        blog_search.write(blog_answer)

if __name__ == "__main__":
    main()
