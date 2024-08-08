from scrape.operations import start_service
from settings import init_driver


if __name__ == "__main__":
    
    
    # Un-comment this if you want to extract new stories' links for the following list of tags
    # tags = ["vampire"]
    # start_service(1, init_driver(), tags)





    # Un-comment this if you want to parse the recently added links and extract the corresponding stories' content
    start_service(2, init_driver())