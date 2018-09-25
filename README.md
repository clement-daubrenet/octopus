# Octopus: A word cloud generator

A word cloud generator: enter an URL and get all the words (verbs and nouns only)
used on that web page. On the admin page, the sum of all the occurrences
of all words parsed.

# General comments

I focused most of my energy on Code design + minimal test coverage + Docker.

Way less on the security aspects (private key in a file, config variables ...)
and the overall frontend side of things that I clearly stole a bit
everywhere on the web.

Warning 1: the private key in a file is a security problem. It should be
at least stored in an environment variable.

Warning 2: I got once an unexpected behavior in the admin (duplicated words
instead of incrementing the same one). I could not reproduce since then
(I think it only happened in the dockerized version).With more time, I would dig into this.


# Docker installation

Just run:

- docker-compose up --build

And you should be happy. Run the app on http://127.0.0.1:8000


# Manual installation:

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


# Tests:

Integration tests for home page:

- python -m pytest tests/tests_home_integration.py

Integration tests for admin page:

- python -m pytest tests/tests_admin_integration.py

Unit tests for home page:

- python -m pytest tests/tests_home_unit.py