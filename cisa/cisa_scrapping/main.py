from scrape.operations import start_service
from settings import init_user_agent


if __name__ == "__main__":
    
    
    # Un-comment this to extract the latest added advisory links that were not added to the archive
    # start_service(1, init_user_agent())
    
    
    
    # Un-comment this to extract the soup of the advisories that need to be parsed
    start_service(2, init_user_agent())