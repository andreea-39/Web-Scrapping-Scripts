from scrape.service import extract_links_for_authors_categories, get_links_for_authors_categories, extract_authors_links_based_on_category, get_authors_links, extract_stories_for_author



def create_options_dictionary(dictionary):
    options = list(dictionary.keys())
    options_dict = {}
    for index in range(len(options)):
        options_dict[index+1] = options[index]
    return options_dict

def start_service(flag, driver):
    if flag == 1:
        extract_links_for_authors_categories(driver)
        
    elif flag == 2:
        links_for_authors_categories = get_links_for_authors_categories()
        
        if len(links_for_authors_categories)<1:
            print("There are no links available for searching authors")
            return
            
        options_dict = create_options_dictionary(links_for_authors_categories)
        options = list(options_dict.values())
            
        print(f"Please input one number from {1} to {len(options)} to select a category or 0 to exit")
        for index in range(len(options)):
            print(f"{index+1}-{options[index]}")
            
        print("0-Exit")
        
        while True:
            try:
                choice = int(input("choice: "))
                if choice == 0:
                    break
                elif choice in options_dict.keys():
                    print(f"Adding new authors for category:  {options_dict[choice]}")
                    extract_authors_links_based_on_category(driver, links_for_authors_categories[options_dict[choice]])
                    
                else:
                    print("Please enter a valid choice")
                
            except:
                print("Please enter a valid integer choice")
            
        
            
    elif flag == 3:
        authors_links = get_authors_links()
        if len(authors_links)<1:
            print("There are no authors available for stories extraction")
            return
        
        options_dict = create_options_dictionary(authors_links)
        options = list(options_dict.values())
            
        print(f"Please input one number from {1} to {len(options)} to select an author or 0 to exit")
        for index in range(len(options)):
            print(f"{index+1}-{options[index]}")
            
        print("0-Exit")
        
        while True:
            try:
                choice = int(input("choice: "))
                if choice == 0:
                    break
                elif choice in options_dict.keys():
                    print(f"Extracting stories for author:  {options_dict[choice]}")
                    print(authors_links[options_dict[choice]], options_dict[choice])
                    extract_stories_for_author(driver, authors_links[options_dict[choice]], options_dict[choice])
                    
                else:
                    print("Please enter a valid choice")
                
            except:
                print("Please enter a valid integer choice")