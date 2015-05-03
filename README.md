# flask_whoosh
A simple python Flask application that runs a data-scraper and a Whoosh search engine implementation. I wrote this mainly to scrape financial news (title, publication datetime, brief summary) off a RSS feed and index the data into the Whoosh search engine. Just a small hobby project to try out new stuff. 

<h3>Pre-requisites</h3>
BeautifulSoup - http://www.crummy.com/software/BeautifulSoup/bs4/doc/ </br>
Flask - http://flask.pocoo.org </br>
Whoosh - https://pypi.python.org/pypi/Whoosh/ </br>

All of the above-mentioned can be installed via pip. Eg. 'pip install Whoosh'

<h3>Instructions</h3>
1. Install the needed dependencies </br>
2. Add the url of RSS feed you wish to scrape, ie. line 85, server.py. Note that you might have to change scrape() to cater to particular RSS feeds' XML
3. Run the server with 'python server.py'. Default port for Flask will be 5000 </br>
The data should be scraped and indexed, new files will be added to '/data' folder </br>

<h3>Usage</h3>
1. To search for a particular term, head to 'locahost:5000/search/<term>'. The top search results will be returned in JSON format with the key being the document ID and the body, the document itself. </br>
2. To scrape the data again, say on another day, head to 'localhost:5000/scrape'. If successful, you will be returned with a 200 OK. </br>
3. To re-index the data, head to 'localhost:5000/index'. If successful, you will be returned with a 200 OK. <br/>

<h3>Example</h3>
Search term : <b>king</b> </br>
Result : </br>
	{ </br>
 12: "'Candy Crush' maker King serves up bittersweet results, shares fall <br/>Wed, 07 May 2014 20:02:56 GMT - King Digital Entertainment Plc's stock plummeted more than 13 percent on Wednesday as signs that the company may be losing steam overshadowed better-than-expected quarterly results from..." </br>
	} </br>
