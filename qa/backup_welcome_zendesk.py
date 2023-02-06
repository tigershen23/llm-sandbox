# References https://developer.zendesk.com/documentation/help_center/help-center-api/using-the-help-center-api/backing-up-your-knowledge-base-with-the-help-center-api/#code-complete

import os
import datetime
import csv

import requests

credentials = "tiger@experiencewelcome.com", os.environ.get("ZENDESK_PASSWORD")
print(credentials)
zendesk = 'https://experiencewelcome.zendesk.com'
language = 'en'

date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

endpoint = zendesk + '/api/v2/help_center/{locale}/articles.json'.format(locale=language.lower())

response = requests.get(endpoint, auth=credentials)

print(response.status_code)
print(response.json())
