# Reading json and text files and parsing the needed information
# Combining the information into a list of dictionaries
# Indexing data to Solr

# import pysolr
import json
import os
import re

# Setting up Solr, note the port number
# solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10, auth= < type of authentication >)

# Making a list for all email dictionaries
emails = []
subject = "subject"
body = "body"
combinations = {}

json_postit = "./json_postit/"
file_number = ""
emails = {}

# json_file in with is and file object, file handle
for filename in os.listdir(json_postit):
    file_number = re.search('^[0-9]+', filename)  # regex
    json_postit_filename = json_postit + filename
    if os.path.isfile(json_postit_filename) \
            and filename.endswith(".json") \
            and not filename in json_files:
        with open(json_postit_filename, encoding="utf-8") as json_file:
            data = json.load(json_file)
            # Finding the value of the subject field from the json file
            subject_name = data["subject"]
            # Combining the subject and body values into an email dictionary
            email = {'subject': subject_name}
            emails = {file_number: email}
            # Appending the email values to the list

print(emails)
# Add texty values for existing subject keys
# Note that there might be a different number of json and txt files in the directory!
# The json and txt files need to correspond to each other

# email_bodies=[]

text_postit = "./text_postit/"
for filename in os.listdir(text_postit):
    file_number = re.search('^[0-9]+', filename)  # regex
    text_postit_filename = text_postit + filename
    if os.path.isfile(text_postit_filename) \
            and filename.endswith(".txt") \
            and not filename in txt_files:
        with open(text_postit_filename, "r", encoding="utf-8") as txt_file:
            body_text = txt_file.read()
            if file_number in emails:
                email = emails[file_number]
                email['body'] = body_text
                emails[email] = email

            else
                email_body = {'body': body_text}
                emails = {file_number: email_body}

print(bodies[0])

# Indexing emails to solr
# solr.add(emails)
