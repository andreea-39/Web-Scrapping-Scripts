
import json
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



current_directory = os.path.join("literotica_scrapping", "scrape")

literotica_authors_main_page_link = "https://www.literotica.com/a/"

def get_links_for_authors_categories():
    with open(os.path.join(current_directory, "utils", "links_for_authors_categories.json")) as infile:
        links_for_authors_categories = json.load(infile)
        
    return links_for_authors_categories

def get_authors_links():
    with open(os.path.join(current_directory, "utils", "authors_links.json")) as infile:
        authors_links = json.load(infile)
        
    return authors_links

def extract_links_for_authors_categories(driver):
    print("Searching for new authors categories links and updating the outdated links")
    with open(os.path.join(current_directory, "utils", "links_for_authors_categories.json")) as infile:
        links_for_authors_categories = json.load(infile)
        
    driver.get(literotica_authors_main_page_link)
    authors_categories_element = driver.find_element(By.CLASS_NAME, "b-cat-filter")
    
    for list_item in authors_categories_element.find_elements(By.TAG_NAME, 'li'):
        try:
            
            link = list_item.find_element(By.TAG_NAME, 'a')
            link = link.get_attribute("href")
            
            # If category already in the dict, update its link if its the case; if not, new dict entry will be added
            links_for_authors_categories[list_item.text] = link
            
            print(f"{list_item.text} - {link}")
        except:
            pass
        
    with open(os.path.join(current_directory, "utils", "links_for_authors_categories.json"), "w") as outfile:
        outfile.write(json.dumps(links_for_authors_categories))
    
    
    
def extract_authors_links_based_on_category(driver, link):
    with open(os.path.join(current_directory, "utils", "authors_links.json")) as infile:
        authors_links = json.load(infile)
    driver.get(link)
    
    for author_item in driver.find_elements(By.CLASS_NAME, 'b-user-info-name'):
        author_link = author_item.find_element(By.TAG_NAME, 'a').get_attribute("href")
    
        if author_item.text not in authors_links.keys():
            print(f"Added author {author_item.text}")
        authors_links[author_item.text] = author_link
        
        with open(os.path.join(current_directory, "utils", "authors_links.json"), "w") as outfile:
            outfile.write(json.dumps(authors_links))
            

def extract_story_content(driver, link):
    driver.get(link)
    visited_urls = [link]
    
    
    story_info = driver.find_element(By.ID, "tabpanel-info").text.split("\n")[0]    
    story_text = {}   
    
    page_number = 1
    
    next_page_button_available = True
    while next_page_button_available == True:
        try:
            print(f"Extracting text for page {page_number}")
            # extract text
            story_text[f"page_number_{page_number}"] = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[5]/div[1]/div[1]/div[4]").text
            page_number+=1

            visited_urls.append(driver.current_url)
            next_page_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[5]/div[1]/div[2]/div/div/a[1]")
            next_page_button.click()
            
            if driver.current_url in visited_urls:
                next_page_button_available = False
        except:
            next_page_button_available = False
    
    return story_info, story_text
            
            
def extract_stories_for_author(driver, link, author_name):
    try:
        driver.get(link+"/works/stories")
        
        stories_info = []
        
        stories_element = driver.find_element(By.CLASS_NAME, "_works_wrapper_14spp_1")
        

        
        for story in stories_element.find_elements(By.CLASS_NAME, "_works_item__title_14spp_36"):
            story_name = story.text
            print(story_name)
            story_link = story.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            stories_info.append({
                "author_name": author_name,
                "story_name": story_name,
                "story_link": story_link
            })
            
        for index in range(len(stories_info)):
            story_name = stories_info[index]["story_name"]
            print(f"Started extracting story: {story_name}")
            story_info, story_text = extract_story_content(driver, stories_info[index]["story_link"])
            stories_info[index]["story_info"] = story_info
            stories_info[index]["story_text"] = story_text
            print("Finished extracting story")
        
            with open(os.path.join("literotica_scrapping", "output", f"{author_name}.json"), "w") as outfile:
                outfile.write(json.dumps(stories_info))
        
    except:
        print("This author does not have published stories")