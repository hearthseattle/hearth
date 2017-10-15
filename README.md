[![Coverage Status](https://coveralls.io/repos/github/kurtrm/homeless_to_hearth/badge.svg?branch=kurt-test-coveralls)](https://coveralls.io/github/kurtrm/homeless_to_hearth?branch=kurt-test-coveralls) [![Build Status](https://travis-ci.org/kurtrm/homeless_to_hearth.svg?branch=master)](https://travis-ci.org/kurtrm/homeless_to_hearth)

# Hearth Seattle Project

   Seattle has the third largest homeless population in the country. Fortunately, it also has some of the best and numerous 
resources to offer people in need. As organizations continue to pop up and support networks grow, it is becoming increasingly
difficult to guide people to the organizations that can meet their specific needs. This project aims to address this problem 
in the following ways:

   - Aggregate resources into **one**, **reliable** web application

   - **Categorize organizations** based on the specific care they provide

   - **Tailor effective search results** based on individual needs

Our ultimate goal is to connect people in need to the care they require as quickly and easily as possible.


### Contributing to Hearth

Hearth has been built on the Django Web Framework, styled with Bootstrap, and deployed to AWS using Ansible. It is a collaborative project that always needs your help for improvement. If you think you can contribute to the project, please take a look at the issues tab and tackle whatever issues you feel you are equipped to handle. Our long term goal is to transition to a React or Vue front end with Django Rest Framework (DRF) on the backend and to completely move away from using Django templates.

### Prerequisites

To make the project as accessible as possible, we are transitioning to a Vagrant environment setup. We'll have steps to use this tool soon.

### Installing
To clone our repository, run the following command:

    git clone https://github.com/hearthseattle/hearth.git

Set up an environment using the following command:

    python3 -m venv ENV

Activate your environment with:

    source ENV/bin/activate

Navigate into the **hearth** (root) directory then run the following command in order to install the required dependencies:

    pip install -r requirements.txt
    
Ensure you have postgreSQL installed and create a database:

    createdb (whatever-you-name-your-database)

Set the following environment variables by opening ENV/bin/activate in your preferred text editor:

    export SECRET_KEY='(secret_key_of_your_choice)'
    export DATABASE_NAME='(name_of_your_database)'
    export DATABASE_PASSWORD='(password_if_required)'
    export DATABASE_HOST='(127.0.0.1)'
    export DATABASE_USERNAME='(username_if_required)'
    export DEBUG='True'
 
Navigate to the same director as manage.py and tell Django to setup your models in the database:

    ./manage.py makemigrations

Then:

    ./manage.py migrate

Feel free to visit the Django [tutorial](https://docs.djangoproject.com/en/1.11/intro/) to gain some familiarity.
   

## Running the tests
Run the following command in the same directory as the **manage.py** file to run tests:

    ./manage.py test


## Built With

    - Django
    - Django Rest Framework
    - Bootstrap.js


## Versioning

Version 0.0

## Authors

* **Kurt Maurer**
* **Ophelia Yin**
* **Anna Shelby**
* **Carlos Cadena**
* **Miguel Pena**
* **Casey O'Kane**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Robert Snow**
* **Austin Briggs**
* **Wes Moore**
* **James Warren**
