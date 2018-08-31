# Dialogue Analysis Systems API (DASA)
## Midterm Project
##### Brandon Haynes, Chris Turner, Liz Mahoney, Max McFarland
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
