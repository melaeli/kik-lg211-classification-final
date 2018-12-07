from flask import Flask, render_template, request, redirect, url_for
from urllib.request import *

#selaimeen: http://localhost:8000/solr/
#lisätty wikiin from urllib.request import *
#huom.Dimalla from urllib, joka toimii Diman esimerkkiin: https://github.com/DmitryKey/kik-lg211-2018/blob/master/flask-solr/flaskdemo.py
#Mathiaksella from urllib.request, joka toimii toiseen wiki-vaihtoehtoon ks. flaskdemo_wiki_dima.py - jälkimmäisellä toimii http://localhost:8000/search


#Initialize Flask instance
app = Flask(__name__)

example_data = [
    {"name": "Cat sleeping on a bed", "source": "cat.jpg"},
    {"name": "Misty forest", "source": "forest.jpg"},
    {"name": "Bonfire burning", "source": "fire.jpg"},
    {"name": "Old library", "source": "library.jpg"},
    {"name": "Sliced orange", "source": "orange.jpg"}
]

#Use "query" variable from the URL. If no variable is given,
#use empty string instead. GET and POST methods are allowed.
@app.route("/search", defaults={"query": ""}, methods=["GET", "POST"])
@app.route("/search/<query>", methods=["GET", "POST"])
def search(query):

    if request.method == "POST":
        #Get query from the POST form.
        query = request.form["query"]

        #Redirect to the same page with the query in the url.
        #ALWAYS REDIRECT AFTER POSTING!
        return redirect(url_for("search", query=query))

    matches = []

    #If an entry name contains the query, add the entry to matches.
    if query != "":
        for entry in example_data:
            if query.lower() in entry["name"].lower():
                matches.append(entry)

    #Render index.html with matches variable.
    return render_template("index.html", matches=matches)


#miksi defaults={"query": "cat"} in https://github.com/DmitryKey/kik-lg211-2018/blob/master/flask-solr/flaskdemo.py - KOSKA URL?
#JOS defaults={"query": ""} kuten in def(search) ja Mathiaksen esimerkillä niin antaa ERROR: urllib.error.HTTPError: HTTP Error 400: Bad Request
#JOS defaults={"query": "Testi"} niin antaa tyhjän aloitussivun; JOS defaults={"query": "Testi_body"} niin antaa hakutuloksen jo päivittäessä sivun - mitä tähän kuuluisi laittaa?
@app.route("/solr/", defaults={"query": "Testi"}, methods=["GET", "POST"])  #Dimalla "/solr", joka antoi errorin: Not Found  
@app.route("/solr/<query>", methods=["GET", "POST"])
def solr(query):
    if request.method == "POST":
        #Get query from the POST form.
        query = request.form["query"]

        #Redirect to the same page with the query in the url.
        #ALWAYS REDIRECT AFTER POSTING!
        return redirect(url_for("solr", query=query))

    matches = []

#laita näin omaan demoon kuten Dimalla:
#    url = 'http://localhost:8983/solr/wiki/select?q=text:' + query + '&wt=python&start=0&rows=10&fl=title,id,text&hl=on&hl.fl=text&hl.simple.post=</b>&hl.simple.pre=<b>'
#    print(url)
#    connection = urlopen(url)

#Mathiaksella:
#    connection = urlopen('http://localhost:8983/solr/wiki/select?q=text:cheese&wt=python&start=0&rows=100')

#HUOM. text:Testi_body PITÄÄ OLLA TÄYSIN SAMASSA MUODOSSA, pelkkä text:testi ei löydä mitään!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Korjaa?
#    connection = urlopen('http://localhost:8983/solr/email/select?q=text:Testi_body&wt=python&start=0&rows=100')

#    connection = urlopen('http://localhost:8983/solr/email/select?q=text:' + query + '&wt=python&start=0&rows=100') # defaults={"query": ""}
#ERROR: urllib.error.HTTPError 400: Bad Request

#    connection = urlopen('http://localhost:8983/solr/email/select?q=text:' + query + '&wt=python&start=0&rows=10&fl=subject,text&hl=on&hl.fl=text&hl.simple.post=</b>&hl.simple.pre=<$'
#ERROR: response = eval(connection.read())  SyntaxError: invalid syntax
#           ^

#hakusana löytää vain tekstikentän eli hakusanalla Teksti_body (ei tulosta, jos hakee Testi, vaikka se on subjektina) - miten löytäisi myös subjectilla???
    url = 'http://localhost:8983/solr/email/select?q=text:' + query + '&wt=python&start=0&rows=10'
#    url = 'http://localhost:8983/solr/email/select?q=text:Testi_body&wt=python&start=0&rows=100'
#urllib.error.HTTPError: HTTP Error 400: Bad Request
    print(url)
    connection = urlopen(url)

    response = eval(connection.read())

    print(response['response']['numFound'], "documents found.")

###ERROR in Dima's code: missing parentheses
#    print ("=========================")
#    print (response['highlighting'])
#    print ("=========================")
###

    # Print the name of each document.

    print("Printing 100 top documents:")

    for i, document in enumerate(response['response']['docs']):
        print(" Email subject ", i, "=", document['subject'])

#tai kuten Dimalla:
#        # print("  Document title ", i, "=", document['title'])
#        id = document['id']
#        print ("id=" + id)
#        # print(response['response']['highlighting'][id])
#        highlight = response['highlighting'][id]['text'][0]
#        match = {"title": document['title'], "text": highlight}


#Exctracting emails einstead of wiki documents title/text or pictures in def search(query)
#OUR PROJECT: solr schemaan subject (done), jotta saadaan ['subject'] tähän:
        match = {"subject": document['subject'], "text": document['text']}
        matches.append(match)

    #Render index.html with matches variable.
    return render_template("index.html", matches=matches)
#tai solr.html, jos teet sennimisen uuden templaten, tai minulla ks. templates/index_wiki.html


#Core email tehty (ei tarvetta input kansiolle, koska meidän oma ohjelma vie sinne yksitellen) ja kopioitu schema wikistä ja muutettu fieldit meille sopivaksi
#pysolr toimimaan pycharmiin done 7.12.2018
#TODO:
#form solr objects: iterointi, jossa käydään dictionaryt läpi ja luodaan solr objektit, jotka listassa, joka lisätään solr.add
#(filenro dict, jonka alla dict, jossa subj ja body - huom vaihda body text:ksi, jotta field löytää
#solr.add sis. subj ja text
#lisää themes extraction, ennakoiva syöttö...
#KYSYMYS: Miten Flask tajuaa, että juuri flaskdemo.py käytössä eikä joku muu saman kansion .py?
