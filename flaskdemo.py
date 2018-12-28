from flask import Flask, render_template, request, redirect, url_for
from urllib.request import *

#Open Solr and Flask in localhosts 8000/8983 and put into browser: http://localhost:8000/solr/ and http://localhost:8983/solr - core email

#Initialize Flask instance
app = Flask(__name__)


#Copied from the code of Otto and Juuso, thank you guys!
#€ does not get an error code but is not included to the search after all
#Replaces whitespaces with a plus and fixes the ascii problem with ääkköset in the query (åäöüÅÄÖÜ) and with euro sign
def addplusaakkoset(query):
    fixed = query.replace(" ", "+").replace("ä", "%C3%A4").replace("ö", "%C3%B6").replace("å", "%C3%A5").replace("ü", "%C3%BC").replace("Ü", "%C3%9C").replace("Ä", "%C3%84").replace("Ö", "%C3%96").replace("Å", "%C3%85").replace("€", "%E2%82%AC")
    return fixed


#Exctracting emails subject/text instead of wiki documents title/text (done in class) or pictures in def search(query) (in example demo)
#defaults={"query": "This_is_not_Supposed_to_Match_Anything"} works -> this is changed into an empty string which finally worked with ""
#Use "query" variable from the URL. If no variable is given, use empty string instead. GET and POST methods are allowed.
@app.route("/solr/", defaults={"query": '""'}, methods=["GET", "POST"])
@app.route("/solr/<query>", methods=["GET", "POST"])
def solr(query):
    if request.method == "POST":
        #Get query from the POST form.
        query = request.form["query"]

        #Redirect to the same page with the query in the url.
        #ALWAYS REDIRECT AFTER POSTING!
        return redirect(url_for("solr", query=query))

    matches = []
    count=0

    # Some of the common words like JA and OVAT don't work in the search because Solr stemms them into nothing
    # Search both from the subject and the text including SPACE
    # Searches the words separately without "" which is instructed in the HTML file; juhla NOT talven search works, too
    url = 'http://localhost:8983/solr/email/select?q=(subject:(' + addplusaakkoset(
        query) + ')+OR+text:(' + addplusaakkoset(query) + '))&wt=python&start=0' + \
          '&rows=100&fl=text,subject,id&hl=on&hl.fl=text&hl.simple.post=</b>&hl.simple.pre=<b>'

    # Trying to add highlighting with Mathias but didn't get it to work (hl.method, hl.fraqsize); leaving the code here anyways for the possible development
    #    url = 'http://localhost:8983/solr/email/select?q=(subject:(' + addplusaakkoset(query) + ')+OR+text:(' + addplusaakkoset(query) + '))&wt=python&start=0&rows=100&$

    print(url)
    connection = urlopen(url)

    response = eval(connection.read())

    #A little bit confusing because having the same name: response['response']...
    print(response['response']['numFound'], "documents found.")

#    print (response['highlighting'])

    #Print the name of each document. This is shown in the shell where the Flask is opened like the print(url) and the for loop below and the print (count).
    print("Printing 100 top documents:")


    for i, document in enumerate(response['response']['docs']):
        print(" Email subject ", i, "=", i+1, document['subject'])


#Testing highlighting: gave html tags without bolding the text itself and only the row where the (first) bolding word occurred - not used in the programme now
#Checked from Solr q, fl, hl, wt etc. but didn't get it work here, needs more investigating...
#To make higlighting to work, the subject and text must be retrieved from different places to the matches
#ID is propably giving by Solr and must be included with highlighting
        # print("  Document title ", i, "=", document['title'])
        id = document['id']
        print ("id=" + id)
        if len(response['highlighting'][id])==0:
            highlight = document['text']
        else:
            highlight = response['highlighting'][id]['text'][0]


#Subject field put into the Solr Schema file; core email done in Solr, no need for input file/folder as the program takes the files there one by one; no need for han$
#        match = {"subject": document['subject'], "text": highlight}

        #Adding the search result count in front of every result in UI
        count=count+1
        match = {"count": count, "subject": document['subject'], "text": document['text']}

        matches.append(match)
        print (count)

    #Render index.html with matches variable.
    return render_template("index.html", matches=matches, n=response['response']['numFound'])
