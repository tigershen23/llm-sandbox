# cSpell:disable
# MAKE SURE YOU'VE RUN THE CRAWLERS BEFORE RUNNING THIS APP OR IT WON'T WORK

# Copy/paste prompts
# What are some features of Welcome that help engage an audience?
# What can you do with Agenda Builder in Welcome?
# What are the recommended dimensions for event cover images on Welcome?

import os
path = os.path.dirname(__file__)

from PIL import Image
import streamlit as st

import qa_exploration as qae

def hide_streamlit_img_full_screen():
    hide_img_full_screen = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''

    return st.markdown(hide_img_full_screen, unsafe_allow_html=True)

def main():
    welcome_logo = Image.open(path + "/static/welcome_light.png")
    st.image(welcome_logo, width=200)
    hide_streamlit_img_full_screen()

    st.markdown("""
    # What is this?

    Yesterday I loaded up some public info on Welcome (marketing site, blog, and Zendesk) into a little
    question-and-answer interface.

    I wanted to share it in the spirit of experimentation even though it's far, far from perfect (slow, can hallucinate,
    etc etc -- don't get your
    expectations up!)

    What stood out to me was how much the infrastructure and tooling has evolved around Language Models. This type of
    thing would have been basically impossible for 1 person to do just a few years ago, let alone in just one day. I'm
    looking forward to seeing where it branches out!

    Let me know what sorts of silly or spot-on responses you're able to get out of this thing.

    Some prompts to get you started:

    * What are some features of Welcome that help engage an audience?
    * What can you do with Agenda Builder in Welcome?
    * What are the recommended dimensions for event cover images on Welcome?

    :tiger:
    """)

    st.write("━" * 40)

    st.markdown("# Welcome...\"in a (text) box\"")
    combined_search = st.container()
    combined_query = combined_search.text_input(
        "Welcome Q&A",
        '',
        placeholder='Ask anything! Ex: What CRMs does Welcome integrate with?',
        key="Combined Q&A text input",
        label_visibility="collapsed"
    )

    st.markdown("<br/><br/><br/>", unsafe_allow_html=True)
    previous_combined_query = ""
    if combined_search.button("Go!", key="Combined Go button") or combined_query != previous_combined_query:
        previous_combined_query = combined_query
        with st.spinner("Spinning the hamster..."):
            combined_agent = qae.get_combined_agent()
            combined_answer = combined_agent.run(combined_query)
        combined_search.write(combined_answer)


    with st.expander("Smaller models"):
        st.caption("In case you want to tinker with the different datasets the main input is drawing from, these will likely run faster since they're only querying a single data source")
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
                marketing_site_agent = qae.get_marketing_site_agent()
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
                blog_agent = qae.get_blog_agent()
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
                zendesk_agent = qae.get_zendesk_agent()
                zendesk_answer = zendesk_agent.run(zendesk_query)
            zendesk_search.write(zendesk_answer)

    with st.expander("Transcript models"):
        st.caption("These models have loaded up event transcripts from various events")
        st.subheader("Welcome Marketing Event Transcripts Q&A [https://www.experiencewelcome.com/events](https://www.experiencewelcome.com/events)")
        marketing_webinar_transcripts_search = st.container()
        marketing_webinar_transcripts_query = marketing_webinar_transcripts_search.text_input(
            'Ask a question about anything from a Welcome Webinar!',
            '',
            placeholder='Ex: Give me a quote about multi-threading in sales deals.'
        )

        previous_marketing_webinar_transcripts_query = ""
        if (marketing_webinar_transcripts_search.button("Go!", key="Marketing Webinar Transcripts Go button") or
            marketing_webinar_transcripts_query != previous_marketing_webinar_transcripts_query):
            previous_marketing_webinar_transcripts_query = marketing_webinar_transcripts_query
            with st.spinner("Analyzing voices..."):
                marketing_webinar_transcripts_agent = qae.get_transcripts_agent()
                marketing_webinar_transcripts_answer = marketing_webinar_transcripts_agent.run(marketing_webinar_transcripts_query)
            marketing_webinar_transcripts_search.write(marketing_webinar_transcripts_answer)

if __name__ == "__main__":
    main()
