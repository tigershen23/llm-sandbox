#!/bin/bash

docker pull webrecorder/browsertrix-crawler

ROOT_URL='https://experiencewelcome.zendesk.com/hc/en-us'

docker run -v $PWD/crawls:/crawls/ -it webrecorder/browsertrix-crawler crawl  \
  --url $ROOT_URL \
  --text \
  --collection welcome_zendesk \
  --scopeType domain  --allowHashUrls
