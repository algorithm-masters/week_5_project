from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='json', request_method='GET')
def home_view(request):
    """Displays the landing page of this webpage. This shows the possible API calls

        Args:
            requst- This is the GET request that is linked to the '/' path, which is the
                    landing page.
        Return:
            A message containing the possible api route calls
    """
    message = """Welcome to the Dialogue Analysis Systems API (DASA)!
    Routes:

    'POST - api/v1/auth/register - BODY:{"email": "**Your Email Here**", "password": "**Your Password Here**"}
        -> This route will register an account in the database and return a session bearer token.

    'POST - api/v1/auth/login - BODY:{"email": "**Your Email Here**", "password": "**Your Password Here**"}
        -> This route will login to an existing account in the database and return a session bearer token.
    
    'POST - api/v1/analysis - BODY:{"text": "**Your Text Here**"}
        -> This route will take in text and return a sentiment analysis using NLTK. 
        -> Each sentence will be analyzed for sentiment, as well as the entire body of the text.
        
    'GET - api/v1/users
        -> This route will return the email and database ID of all users registered in the database.

    'GET - api/v1/charts/{graph_type}
        -> This route will return all of the analysis that are stored in the database for the user logged in.
        -> {graph_type}: stacked_bar
    
    'DELETE - api/v1/admin/delete/{user_id} - {"email": "**Admin Email**", "password": "**Admin Password**"}
        -> This route will delete a singe user based on database id. Only admins can access this route.

    'GET - api/v1/admin/{graph_type}/{id}
        -> This route will retrieve all of a users data if their ID is specificed.
        -> This route will retrieve all of the aggregate data from the website if no ID is specified.
        -> This route is Admin access only.
        -> {graph_type}: stacked_bar, compound_bar, pie

    """
    return Response(body=message, content_type='text/plain', status=200)




