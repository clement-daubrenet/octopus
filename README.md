# Octopus: A word cloud generator

A word cloud generator: enter an URL and get all the words (verbs and nouns only)
used on that web page. On the admin page, the sum of all the occurrences
of all words parsed.

## 1. Demonstration

Paste an URL in the search bar:

![Alt text](/docs/step0.png?raw=true "Search Bar")

Then, "generate" will generate a word cloud for you (the bigger the word, the more often it appears):

![Alt text](/docs/step4.png?raw=true "Word Cloud")

Eventually the admin tab will give you the total count of words (e.g: generating 2 times the same word cloud will double 
the current count):

![Alt text](/docs/step5.png?raw=true "Word Cloud Admin")



## 2. General comments

I focused most of my energy on code design + minimal test coverage + Docker.

Way less on the security aspects (private key in a file, config variables ...)
and the overall frontend side of things that I clearly stole a bit
everywhere on the web.

Warning 1: the private key in a file is a security problem. It should be
at least stored in an environment variable.


## 3. Docker installation

Just run:

- docker-compose up --build

And you should be happy. Run the app on http://127.0.0.1:8000

Warning 2: You might have to change the ports (in the docker-compose.yml) of the web app and database depending on the allocations on your machine.
I tested this app on 2 different machines and had to change the ports (e.g: 8000 to 8001 and 5000 to 6000).

## 4. Manual installation:

If things go wrong and you want to do it old school:

Create a virtualenv:

- virtualenv env -p python3

Source the virtualenv:

- source env/bin/activate

Install the requirements:

- pip install -r requirements.txt

Install mysql to connect with following URL: 'mysql://root:rootroot@localhost:3306/octopus'
Download the corpus packages for stopwords and tokenizer, in a python interpreter:

- import nltk
- nltk.download('stopwords')
- nltk.download('punkt')

Launch the server:

- python manage.py

Start using the web page:

- By default, go on http://127.0.0.1:8888/


## Tests:

Integration tests for home page:

- python -m pytest tests/tests_home_integration.py

Integration tests for admin page:

- python -m pytest tests/tests_admin_integration.py

Unit tests for home page:

- python -m pytest tests/tests_home_unit.py
