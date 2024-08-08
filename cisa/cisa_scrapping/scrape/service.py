import pickle
import requests
from bs4 import BeautifulSoup
import os
import json
import re

current_directory = os.path.join("cisa_scrapping", "scrape")

main_page_link = "https://www.cisa.gov/news-events/cybersecurity-advisories"

advisory_base_link = "https://www.cisa.gov/"

page_base_link = "https://www.cisa.gov/news-events/cybersecurity-advisories?page="


def extract_new_advisory_links(user_agent):
    
    with open(os.path.join(current_directory, "utils", "links_archive", "links_that_need_to_be_parsed.json"), "r") as infile:
        links_that_need_to_be_parsed = json.load(infile)
    
    with open(os.path.join(current_directory, "utils", "links_archive", "parsed_links.json"), "r") as infile:
        parsed_links = json.load(infile)
        
    
    headers = {
            "User-Agent": user_agent.random,
        }
    
    # all the updates will be added on the first page    
    page_number = 1
    
    # flag that determines when the next page option is still valid
    valid_page = True
    
    # besides the 'valid_page' flag, this is used to determine when the algorithm should stop(when there are no new advisories to parse)
    new_advisory_link = True
    
    
    while valid_page and new_advisory_link == True:
        print(f"Parsing page number: {page_number}")
        page_link = page_base_link + str(page_number)
        page = requests.get(page_link, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        
        
        # Search for the html table that contains the links for advisories
        table = soup.find("div", class_="l-sidebar__main")
        table2 = table.find(
            "div",
            class_="views-element-container c-block c-block--view c-block--provider-views c-block--id-views-blockindex-advisory-listing-block-1",
        )
        table3 = table2.find("div", class_="c-block__content")

        tableRows = table3.find_all("div", class_="c-view__row")

        if len(tableRows) == 0:
            validPage = False
            break

        # Parse each advisory link
        for tableRow in tableRows:
            advisory_link = advisory_base_link + tableRow.find("a", href=True)["href"]
            
            
            # Check if the advisory link has been parsed in the past
            # if yes, then break the operations
            # if no, then save it to the list
            if advisory_link in parsed_links:
                new_advisory_link = False
                break
            else:
                links_that_need_to_be_parsed.append(advisory_link)        
                print(advisory_link)

        page_number += 1
        
        with open(
            os.path.join(current_directory, "utils", "links_archive", "links_that_need_to_be_parsed.json"), "w"
        ) as outfile:
            outfile.write(json.dumps(links_that_need_to_be_parsed))
            


def determine_next_file_number():
    flag = "old_folder"
    if len(os.listdir(os.path.join("cisa_scrapping", "output", "soup"))) == 0:
        return 1, "new_folder";
    
    highest_number = 1
    for file in os.listdir(os.path.join("cisa_scrapping", "output", "soup")):
        file_number = re.search("\d+", file).group()
        if int(file_number)>=highest_number:
            highest_number = int(file_number)
            
    with open(os.path.join("cisa_scrapping", "output", "soup", f"CISA_advisories_{highest_number}.pickle"), "rb") as infile:
        if len(pickle.load(infile))==16:
            highest_number+=1
            flag = "new_folder"
            
    return highest_number, flag
        
        

def extract_advisory_soup(user_agent):
    headers = {
            "User-Agent": user_agent.random,
        }
    
    with open(os.path.join(current_directory, "utils", "links_archive", "links_that_need_to_be_parsed.json"), "r") as infile:
        links_that_need_to_be_parsed = json.load(infile)
        
    with open(os.path.join(current_directory, "utils", "links_archive", "parsed_links.json"), "r") as infile:
        parsed_links = json.load(infile)
        
    file_number, flag = determine_next_file_number()
    
    if flag == "old_folder":
        with open(os.path.join("cisa_scrapping", "output", "soup", f"CISA_advisories_{file_number}.pickle"), "rb") as infile:
            cisa_advisories_chunk = pickle.load(infile)
    elif flag == "new_folder":
        cisa_advisories_chunk = []
        
        
    while(len(links_that_need_to_be_parsed)>0):
        
        advisory_link = links_that_need_to_be_parsed.pop(0)
        print(f"Extracting text for link: {advisory_link}")
        
        page = requests.get(advisory_link, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        
        cisa_advisories_chunk.append({
            "advisory_link": advisory_link,
            "soup": soup
        })
        
        parsed_links.append(advisory_link)
        
        with open(os.path.join("cisa_scrapping", "output", "soup", f"CISA_advisories_{file_number}"), "wb") as outfile:
            pickle.dump(cisa_advisories_chunk, outfile)
        
        with open(os.path.join(current_directory, "utils", "links_archive", "links_that_need_to_be_parsed.json"), "w") as outfile:
            json.dump(links_that_need_to_be_parsed, outfile)
            
        with open(os.path.join(current_directory, "utils", "links_archive", "parsed_links.json"), "w") as outfile:
            json.dump(parsed_links, outfile)
            
        if len(cisa_advisories_chunk)==16:

            cisa_advisories_chunk = []
                
            file_number+=1