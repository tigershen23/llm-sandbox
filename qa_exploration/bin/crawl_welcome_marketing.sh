#!/bin/bash

docker pull webrecorder/browsertrix-crawler

docker run -v $PWD/crawls:/crawls/ \
  -v $PWD/crawl-config-welcome-marketing.yaml:/app/crawl-config.yaml \
  -it webrecorder/browsertrix-crawler crawl  \
  --config /app/crawl-config.yaml \
  --text \
  --overwrite \
  --workers 4 \
  --collection welcome_marketing \
  --allowHashUrls

# To use scraped data in GPT-Index:
# docs = SimpleDirectoryReader("./crawls/collections/test/pages").load_data()
# website_index = GPTSimpleVectorIndex(docs, llm_predictor=davinci)
