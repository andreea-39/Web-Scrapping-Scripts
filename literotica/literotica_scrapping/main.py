from scrape.operations import start_service
from settings import init_driver



if __name__ == "__main__":
    
    
    # Un-comment this if you want to extract new links for authors' categories and update the outdated ones
    # start_service(1, init_driver())
    
    
    
    #Un-comment this if you want to update the list of authors based on a given category
    # start_service(2, init_driver())
    
    
    #Un-comment this if you want to update the list of stories for a selected author
    start_service(3, init_driver())