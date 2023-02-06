# cSpell:disable
# For now, it's a manual process of updating this file when we make changes to document_qa.ipynb
# MAKE SURE YOU'VE RUN THE CRAWLERS BEFORE RUNNING THIS APP OR IT WON'T WORK

from gpt_index import GPTTreeIndex, GPTListIndex, SimpleWebPageReader, SimpleDirectoryReader, BeautifulSoupWebReader, GPTSimpleVectorIndex
from langchain.agents import load_tools, Tool, initialize_agent, ZeroShotAgent, AgentExecutor
from langchain.llms import OpenAI
from langchain import OpenAI, LLMChain
from PIL import Image
import os
import streamlit as st

path = os.path.dirname(__file__)

#region marketing site supporting code
# Set up document QA index
@st.cache(allow_output_mutation=True)
def get_marketing_site_index():
    welcome_marketing_site_data = SimpleDirectoryReader(path +"/crawls/collections/welcome_marketing/pages").load_data()
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
    llm = OpenAI(temperature=0.0)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
#endregion

#region blog supporting code
# Set up document QA index
@st.cache(allow_output_mutation=True)
def get_blog_index():
    welcome_blog_data = SimpleDirectoryReader(path + "/crawls/collections/welcome_marketing/pages").load_data()
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

#region Zendesk supporting code
# Set up document QA index
@st.cache(allow_output_mutation=True)
def get_zendesk_index():
    welcome_zendesk_data = SimpleDirectoryReader(path + "/data/welcome_zendesk/2023-02-06").load_data()
    welcome_zendesk_index = GPTSimpleVectorIndex(welcome_zendesk_data)

    return welcome_zendesk_index

# Query DB
def query_zendesk_db(query: str):
    return get_zendesk_index().query(query, verbose=True)

# Create LangChain agent
def get_zendesk_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=query_zendesk_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
#endregion

#region combined supporting code
# Set up document QA index
def get_combined_list_index():
    welcome_marketing_site_index = get_marketing_site_index()
    summary = welcome_marketing_site_index.query(
        "What is a summary of these documents?",
    )
    welcome_marketing_site_index.set_text(summary)

    welcome_blog_index = get_blog_index()
    summary = welcome_blog_index.query(
        "What is a summary of these documents?",
    )
    welcome_blog_index.set_text(summary)

    welcome_zendesk_index = get_zendesk_index()
    summary = welcome_zendesk_index.query(
        "What is a summary of these documents?",
    )
    welcome_zendesk_index.set_text(summary)

    return GPTListIndex([welcome_marketing_site_index, welcome_blog_index, welcome_zendesk_index])

def get_combined_tree_index():
    welcome_marketing_site_index = get_marketing_site_index()
    summary = welcome_marketing_site_index.query(
        "What is a summary of these documents?",
    )
    welcome_marketing_site_index.set_text(summary)

    welcome_blog_index = get_blog_index()
    summary = welcome_blog_index.query(
        "What is a summary of these documents?",
    )
    welcome_blog_index.set_text(summary)

    welcome_zendesk_index = get_zendesk_index()
    summary = welcome_zendesk_index.query(
        "What is a summary of these documents?",
    )
    welcome_zendesk_index.set_text(summary)

    return GPTTreeIndex([welcome_marketing_site_index, welcome_blog_index, welcome_zendesk_index])

# Query DB
def query_combined_list_db(query: str):
    return get_combined_list_index().query(query, verbose=True)

def query_combined_tree_db(query: str):
    return get_combined_tree_index().query(query, verbose=True)

# Create LangChain agent
def get_combined_list_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=query_combined_list_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent

def get_combined_tree_agent():
    tools = [
        Tool(
            name="QueryingDB",
            func=query_combined_tree_db,
            description="Returns most relevant answer from document for query string",
        )
    ]
    llm = OpenAI(temperature=0.1)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent
#endregion

def hide_streamlit_img_full_screen():
    hide_img_full_screen = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''

    return st.markdown(hide_img_full_screen, unsafe_allow_html=True)

# Streamlit interface
def main():
    # st.title("Welcome Question-Answering")
    welcome_logo = Image.open(path + "/static/welcome_light.png")
    st.image(welcome_logo, width=200)
    hide_streamlit_img_full_screen()

    st.markdown("""
    # What is this?

    Yesterday I loaded up some public info on Welcome (marketing site, blog, and Zendesk) into a little
    question-and-answer interface.

    I wanted to share it in the spirit of experimentation even though it's far, far from perfect -- don't get your
    expectations up!

    What stood out to me was how much the infrastructure and tooling has evolved around Language Models. This type of
    thing would have been basically impossible for 1 person to do just a few years ago, let alone in just one day. I'm
    looking forward to seeing where it branches out!

    Let me know what sorts of silly or spot-on responses you're able to get out of this thing!

    :tiger:
    """)

    st.write("━" * 40)

    st.subheader("Welcome Marketing Site Q&A")
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

    st.write("━" * 20)

    st.subheader("Welcome Blog Q&A")
    blog_search = st.container()
    blog_query = blog_search.text_input(
        "Ask a question about anything written on Welcome's blog!",
        '',
        placeholder='Ex: What can you do with Agenda Builder in Welcome?'
    )

    previous_blog_query = ""
    if blog_search.button("Go!", key="Blog Go button") or blog_query != previous_blog_query:
        previous_blog_query = blog_query
        with st.spinner("One mississippi, two mississippi..."):
            blog_agent = get_blog_agent()
            blog_answer = blog_agent.run(blog_query)
        blog_search.write(blog_answer)

    st.write("━" * 20)

    st.subheader("Welcome ZenDesk Q&A")
    zendesk_search = st.container()
    zendesk_query = zendesk_search.text_input(
        "Ask a question about any of Welcome's support content!",
        '',
        placeholder='Ex: What are the recommended dimensions for event cover images on Welcome?'
    )

    previous_zendesk_query = ""
    if zendesk_search.button("Go!", key="ZenDesk Go button") or zendesk_query != previous_zendesk_query:
        previous_zendesk_query = zendesk_query
        with st.spinner("Granting wishes..."):
            zendesk_agent = get_zendesk_agent()
            zendesk_answer = zendesk_agent.run(zendesk_query)
        zendesk_search.write(zendesk_answer)

    # st.write("━" * 34)

    # st.header("Welcome Q&A (List)")
    # combined_list_search = st.container()
    # combined_list_query = combined_list_search.text_input(
    #     "Ask about Welcome!",
    #     '',
    #     placeholder='Ex: What 3rd-party platforms does Welcome integrate with?',
    #     key="Combined List Q&A text input"
    # )

    # previous_combined_list_query = ""
    # if combined_list_search.button("Go!", key="Combined List Go button") or combined_list_query != previous_combined_list_query:
    #     previous_combined_list_query = combined_list_query
    #     with st.spinner("Spinning the hamster..."):
    #         combined_list_agent = get_combined_list_agent()
    #         combined_list_answer = combined_list_agent.run(combined_list_query)
    #     combined_list_search.write(combined_list_answer)

    # st.write("━" * 34)

    # st.header("Welcome Q&A")
    # combined_tree_search = st.container()
    # combined_tree_query = combined_tree_search.text_input(
    #     "Ask about Welcome!",
    #     '',
    #     placeholder='Ex: What 3rd-party platforms does Welcome integrate with?',
    #     key="Combined Tree Q&A text input"
    # )

    # previous_combined_tree_query = ""
    # if combined_tree_search.button("Go!", key="Combined Tree Go button") or combined_tree_query != previous_combined_tree_query:
    #     previous_combined_tree_query = combined_tree_query
    #     with st.spinner("Spinning the hamster..."):
    #         combined_tree_agent = get_combined_tree_agent()
    #         combined_tree_answer = combined_tree_agent.run(combined_tree_query)
    #     combined_tree_search.write(combined_tree_answer)

if __name__ == "__main__":
    main()
