# Dialogue Analysis Systems API (DASA)
## Midterm Project
##### Chris Turner, Liz Mahoney, Max McFarland
​
## Requirements
- needs a db (CRUD)
- Needs users and auth/ authentication
- Pryamid app
- use NLTK 
- Headless (send and recv data from httpy or postman)
​
### Our project
- User (signup and add user to db)
- Admin (have special authorization for data analysis)
​
### Use case (user)
- Users hit analysis endpoint with their selected input (string input  250 words) 
- NLTK the input
- Store the data in a db (with ties to the user that sent it)
- Send the response to the user
- Can delete account and responses that are tied to them
​
### Use case (admin)
- Hit a special admin user endpoint to see the data (numpy)
- Manage users as needed (Create - Delete)

### Getting Started

Natural Learning Toolkit- [nltk](http://www.nltk.org/)

Create a db called midterm

Run these commands:
pip install -e ".[testing]"
initialize_dasa_db development.ini


## Getting NLTK to work in the project
Run the nltk setup file in the static folder to download all the needed NLTK sublibraries. 
- you should get a popup window to select the modules to download (see nltk_downloads.png) if needed
- select 'download all'


## Getting Started with Testing 

One time database install for testing:
    -Go to terminal and type:
        > psql
        > CREATE DATABASE dasa_api_test;
            -should see CREATE DATABASE on the command line
        > \c dasa_api_test

To OMIT certain files, Go to .coveragerc file:
   - add path files with **/**/<file name> .coveragerc file.

To run pytest on terminal, go to dasa directory where the pipfile is located then run:
    - pipenv shell
    - pytest --cov=dasa --disable-warnings -v


    
### On AWS:

Setup an RDS postgres database
- config your production.ini with the RDS address/password, etc
- run:
>initialize_dasa_db production.ini

#### To update the EC2:
> cd src 
> git status
> git pull origin master
> pip3 install -e . --user

#### To update the RDS:
> initialize_dasa_db production.ini


#### Restart gunicorn and verify it is working:
> sudo systemctl restart gunicorn
> sudo systemctl status gunicorn

#### To Error check:
> sudo journalctl -xe

#### Clear the RDS tables (if needed)
Connect to the database (needs password):
> psql --host=dasadev2.cktmpeqirhch.us-west-2.rds.amazonaws.com --port=5432 --username=cturner --password --dbname=dasadev2
> drop table account_roles cascade;
> drop table accounts cascade;
> drop table nltk_output cascade;
> drop table nltk_output_id_seq cascade;
> drop table nltk_output cascade;
> drop table roles_association cascade;
