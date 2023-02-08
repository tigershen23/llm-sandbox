# QA

Simple Document QA with GPTIndex and LangChain

4 sources (so far) in `data`:

- Welcome marketing site
- Welcome blog
- Welcome support site
- Welcome marketing event transcripts

### Activate venv and install dependencies (do this first)

```bash
python -m venv .qae_venv
source .qae_venv/bin/activate
cd qa_exploration
python -m pip install
cd ..
python -m pip install
```

### Running Streamlit app

Do this from the root dir to pick up the theme! Streamlit isn't great at handling apps that aren't in the top-level directory, but we'll bear with it.

```bash
streamlit run qa_exploration
```

Visit localhost:8501 for the running app

### Collecting data

There is a version of the experimental dataset from 2023-02-07 included with the repository. To refresh:

#### Welcome website

Run `./bin/crawl_welcome_marketing.sh`

This will give you a `crawls/collections/welcome_marketing...` relative folder in this directory. Find `pages/pages.jsonl` and copy it to `data/website/welcome_marketing/pages/pages.jsonl`

#### Welcome blog

Same process as above, but `s/marketing/blog`

#### Welcome ZenDesk

Set ENV["ZENDESK_PASSWORD"] to zendesk password. If using another user, modify `bin/backup_welcome_zendesk.py` accordingly.

Run `python bin/backup_welcome_zendesk.py`


#### Transcripts

From a machine with heroku logged in to whichever Welcome environment you are pulling from:



### Chatbase

There's a chatbase bot on the "combined" data here, if you want to look for any reason. It's noticeably worse than the
base QA from this repo, that might be due to a higher temperature?
https://www.chatbase.co/chatbot/combined-pdf-4y3fc29rd

### Misc

Python dependencies, why oh why. Saving deps:

```bash
pip list --format=freeze > requirements.txt
```

