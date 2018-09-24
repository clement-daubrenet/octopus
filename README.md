# Octopus: A word cloud generator

A word cloud generator: enter an URL and get all the words (verbs and nouns only)
used on that web page. On the admin page, the sum of all the occurrences
of all words parsed.

# Manual installation:

- Create a virtualenv:

virtualenv env -p python3

- Source the virtualenv:

source env/bin/activate

- Install the requirements:

pip install -r requirements.txt

- Install mysql to connect with following URL:
'mysql://root:rootroot@localhost:3306/octopus'

- Download the corpus packages for stopwords and tokenizer, in a python interpreter:

import nltk
nltk.download('stopwords')
nltk.download('punkt')

- Launch the server:

python manage.py

- Start using the web page:

By default, go on http://127.0.0.1:8888/


# Tests:

- Integration tests for home page:

python -m pytest tests/tests_home_integration.py

- Integration tests for admin page:

python -m pytest tests/tests_admin_integration.py

- Unit tests for home page:

python -m pytest tests/tests_home_unit.py