# import sys
# sys.path.append("..")
# from . import streamlit_app #get_zendesk_agent, get_combined_agent
import qa_exploration as qae

# cProfile.run("profile_zendesk()")
def profile_zendesk():
    zendesk_agent = qae.get_zendesk_agent()
    zendesk_answer = zendesk_agent.run('What are the recommended dimensions for event cover images on Welcome?')
    return zendesk_answer

# cProfile.run("profile_combined()")
def profile_combined():
    combined_agent = qae.get_combined_agent()
    combined_answer = combined_agent.run('What are the recommended dimensions for event cover images on Welcome?')
    return combined_answer

if __name__ == "__main__":
    profile_zendesk()
    # profile_combined()
