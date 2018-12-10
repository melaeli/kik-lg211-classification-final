# Reading json and text files and parsing the needed information
# Combining the information into a list of dictionaries
# Indexing data to Solr

import pysolr
import json
import os
import re
import pprint

# Setting up Solr, note the port number
solr = pysolr.Solr('http://localhost:8983/solr/email', timeout=10)

# Making a list for all email dictionaries
emails = []
subject = "subject"
text = "body"
combinations = {}

json_postit = "./json_postit/"
file_number = ""
emails = {}

# Retrieving the email subjects from the json files
for filename in os.listdir(json_postit):
    file_number = re.search('^[0-9]+', filename)
    file_number = (file_number.group(0))
    json_postit_filename = json_postit + filename
    if os.path.isfile(json_postit_filename) \
            and filename.endswith(".json") \
            and not filename in json_postit:
        with open(json_postit_filename, encoding="utf-8") as json_file:
            data = json.load(json_file)
            # Finding the value of the subject field from the json file
            subject_name = data["subject"]
            # Combining the subject and body values into an email dictionary
            email = {'subject': subject_name}
            emails[file_number] = email


# Adding a default text body to all existing email subject keys
body_text = "Email body not available."
for e in emails:
    email = emails[e]
    email['text'] = body_text
    emails[file_number] = email

# Retrieving the email bodies from the plain txt files
text_postit = "./text_postit/"
for filename in os.listdir(text_postit):
    file_number = re.search('^[0-9]+', filename)
    file_number = (file_number.group(0))
    text_postit_filename = text_postit + filename
    if os.path.isfile(text_postit_filename) \
            and filename.endswith(".txt") \
            and not filename in text_postit:
        with open(text_postit_filename, "r", encoding="utf-8") as txt_file:
            text_body = txt_file.read()
            if not text_body:
                body_text = body_text
                email = emails[file_number]
                email['text'] = body_text
                emails[file_number] = email
            else:
                body_text = text_body
                email = emails[file_number]
                email['text'] = body_text
                emails[file_number] = email


#pprint.pprint(emails)

#print(emails["10"]['subject'] + emails["10"]["text"]) # Test: email body available
#print(emails["1"]['subject'] + emails["1"]["text"])  # Test: email body not evailable, shows default text body

# Creating json files of each email dictionary element
for file_number in emails:
    with open(file_number+"email.json", "w", encoding="utf-8") as f:
        json.dump(emails[file_number], f)

# Indexing emails to Solr as json files
# Need to be tested
for file_number in emails:
    solr.add(file_number+"email.json")
