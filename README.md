#### Commercial email finder 

This is a group project for the University of Helsinki NLP course.
In our project we created an application where you can search commercial email data indexed into Apache Solr.
The email data was first converted into a suitable format and indexed into Solr with Python. For our user interface we used Flask web framework to enable searching from Solr through a web brouwser user interface. HTML was used for styling the interface. 

Our original plan was to create a project around text classification so that each email would be classified into searchable topics. During the project different ways of incorporating the topic search feature arised but was not carried out. Creating a working application required all our efforts but we found studying and weighing different options for email classification or topic recognition as great practice. As the time for project was rather limited, we consider our successful though equally limited. We may have made some better choices on what we decided to work on and what to exclude but we also think we disregarded the features we needed to have a working application within the time limit.


### Installation

NOTE: The email files used for the project are excluded from the repository as the contain sensitive information! 

To use the project with your own email files you can create a pst file of your emails and extract them into separate files with Apache Tika. The `readpst` command creates 2 files of a pst email file: an extentionless file and an rtf file (this only includes). These extentionless files you can transform into json and the rtf files into plain text files with Apache Tika. To index your own email into Solr, run **email_combiner.py** with your file path for your emails.

All other files can be attained by cloning this repository.


## Solr

To use Solr, you need to have Java installed.
 
Install and run Solr on port 8983.

To run Solr:

$ cd solr-7.5.0

$ bin/solr start -p 8983

If you do not initialize your Solr with example schemas you will need to create your own email core and make make the necessary modifications to other files.


## Flask 

To use the application with its browser interface you need to set up and run Flask. For an introduction to Flask, take a look at the instructions by [Mikko Aulamo](https://github.com/miau1/flask-example).


## email_combiner.py

To index your emails into Solr, run email_combiner.py with approriate paths to the folders containing your emails.


## How to run the program 

For example on your local Windows computer for Solr and Linux Ubuntu shell for Flask do this:

1) Start Solr in Windows cmd and go to the Solr folder that you have created

2) Possible needs to set up Java home

3) Start Solr (you may need to go to the bin folder and you may have a different command)

4) If the Solr does not start, stop it with the command solr stop -all and try again

5) Go to your browser and open: localhost:8983


**Commands in cmd:**

C:\solr-7.5.0>set JAVA_HOME=C:\Program Files (x86)\Java\jre1.8.0_181

cd bin

C:\solr-7.5.0\bin>solr.cmd start

6) Start Flask in Linux Ubuntu shell by going to your Flask/myproject folder that you have created and activate your Flask environment

7) Go to the flask-example folder and run the export commands and then flask run

8) Go to your browser and open: localhost:8000/solr


**Commands in Ubuntu shell:**

~/Flask/myproject$ . demoenv/bin/activate 

(demoenv) ~/Flask/myproject$ cd flask-example/

(demoenv ~/Flask/myproject/flask-example$ export FLASK_APP=flaskdemo.py

export FLASK_ENV=development

export FLASK_RUN_PORT=8000

flask run


**Browser:** localhost:8000/solr



You can close Flask with Ctrl+C and deactivate your Flask virtual environment with the command `deactivate`.


