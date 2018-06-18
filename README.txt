geru_challenge README
==================

* Getting Started

This application represents the challenge for the GERU company.

---------------
* Setup project

- cd <directory containing this file>

- install the virtualenvwrapper - pip install virtualenvwrapper
(http://virtualenvwrapper.readthedocs.io/en/latest/install.html)

- build the project: python setup.py develop

- initialize the db setup - python initialize_geru_challenge_db development.ini

- run the project: pserve development.ini

- access the link: http://localhost:6543/

---------------
* URLS
/ = Presents a simple HTML page containing a title that reads "Web Challenge 1.0".

/quotes - Presents a page containing all quotes returned by the API (each contained in its own bullet point).

/quotes/{quote_number} - Presents a page containing the <quote_number> quote returned by the API.

/quotes/random - Present a page containing a random quote. Both the <quote_number> and the quote selected randomly
ought to be displayed.

/get_requests - Find all request in db and return a json response.

/get_requests_by_session/{session_key} - Find all request by session (unique identifier) in db and return a json.

/get_sessions - Find all sessions in db and return a json response.

/get_session/{session_key} - Find only one session by session key in db and return a json response.

---------------
* Tests
- you can run the tests using: python -m pytest geru_challenge
