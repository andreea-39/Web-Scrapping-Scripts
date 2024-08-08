
import json
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


current_path = os.path.join("wattpad_scrapping", "scrape")


"""
    This function takes as an input a list of tags, and starting from the main page it inputs each tag in the search bar, parses the results 
    and presses the load more results button multiple times (default=25) so more stories will be loaded. For each story, its link will be extracted
    and added to a file named 'links_that_need_to_be_parsed.json' in case it is not already presented there or in the 'parsed_links.json' file
"""
def extract_links_by_tags(driver, tags, number_of_load_mode_clicks=25):

    wattpad_mainpage_url = "https://www.wattpad.com/home"
    driver.get(wattpad_mainpage_url)
    # time.sleep(2)

    with open(os.path.join(current_path , "utils", "parsed_links.json"), "r") as infile:
        parsed_links = json.load(infile)
        
    with open(os.path.join(current_path , "utils", "links_that_need_to_be_parsed.json"), "r") as infile:
        links = json.load(infile)
        
    
    for tag in tags:
        print(f"Currently searching stories for tag: {tag}")
        
        # searches for the input field element
        search_input_field = driver.find_element(By.TAG_NAME, "input")
    
        
        # types in the search field the current tag and presses enter
        search_input_field.send_keys(tag)
        search_input_field.send_keys(Keys.ENTER)
        
        if len(driver.find_elements(By.CLASS_NAME, 'empty-search-results'))>0:
            print("No stories resulted for this tag")
            continue

        time.sleep(2)

        # loads more results
        print(f"Load more results for {number_of_load_mode_clicks} times for tag {tag}... ")
        for index in range(number_of_load_mode_clicks):
            try:
                driver.find_element(By.CLASS_NAME, "btn-load-more").click()
                time.sleep(2)
            except:
                print("Failed to load more stories")
            
        results_stories = driver.find_element(By.ID, "results-stories")
        results_stories = results_stories.find_elements(By.TAG_NAME, "li")

        # parses the results
        for story in results_stories:
            try:
                # for each resulted story searched for its link
                link = story.find_element(By.TAG_NAME, "a").get_attribute("href")
                print(link)
                if link not in links and link not in parsed_links:
                    links.append(link)
                    
                    with open(os.path.join(current_path , "utils", "links_that_need_to_be_parsed.json"), "w") as outfile:
                        outfile.write(json.dumps(links))
    #             time.sleep(2)
            except:
    #             time.sleep(2)
                pass




def extract_story_base_info(driver):
    story_title = driver.find_element(By.CLASS_NAME, 'story-info').text.split("\n")[0]
    reads = driver.find_element(By.CLASS_NAME, 'new-story-stats').text.split("\n")[2]
    votes = driver.find_element(By.CLASS_NAME, 'new-story-stats').text.split("\n")[6]
    
    return story_title, reads, votes


def extract_chapter_content(driver):
    wattpad_chapter = {}
    
    # extract chapter title
    chapter_title = driver.find_element(By.TAG_NAME, 'h1')
    chapter_title=chapter_title.text
    wattpad_chapter["chapter_title"] = chapter_title

    time.sleep(2)

    # exract chapter stats: reads, votes and comments(number of comments)
    stats=driver.find_element(By.CLASS_NAME, "story-stats").text.split(" ")
    wattpad_chapter["chapter_stats"] = {
                                        "reads": stats[0],
                                        "votes": stats[1],
                                        "comments": stats[2]
                                      }

    print("Reading chapter: ", chapter_title)

    # parse all the pararaphs, preprocess them and add them to the final string 'paragraphs_text'
    paragraphs_text = " "
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')

    for paragraph in paragraphs:
        rewritten_paragraph = ""

        lines = paragraph.text.split("\n")
        for line in lines:
            line = line.strip()
            # eliminate from the text the number of votes for each paragraph
            if re.compile("\d+").match(line) == None:
                rewritten_paragraph+=line+" "

        paragraphs_text+=rewritten_paragraph + "\n"


    wattpad_chapter["chapter_content"] = paragraphs_text
    
    return wattpad_chapter



# takes as an input a story url and extracts its content
def extract_story_content(driver, url):
    
    driver.get(url)
    
    wattpad_story_chapters = []
    next_chapter_available = True

    time.sleep(2)
    story_title, reads, votes = extract_story_base_info(driver)
    time.sleep(2)
    
    # Start reading the story -> Go to the first page (chapter 1/Prologue)
    start_reading_button_div = driver.find_element(By.CLASS_NAME, 'story-actions')
    start_reading_button = start_reading_button_div.find_element(By.TAG_NAME, 'a')
    start_reading_button.click();
    
    print(f"Started reading story: {story_title}")
    time.sleep(2)

    wattpad_chapter = extract_chapter_content(driver)
    wattpad_story_chapters.append(wattpad_chapter)

    # while there is still a next chapter, jump to the next one and extract its content
    while next_chapter_available == True:
        
        try:

            next_chapter_button = driver.find_element(By.XPATH, "/html/body/div[4]/div/main/article/footer/div[1]/div[1]/div/div/div/a")
            driver.execute_script("arguments[0].click();", next_chapter_button)
            time.sleep(2)

            wattpad_chapter = extract_chapter_content(driver)
            
            wattpad_story_chapters.append(wattpad_chapter)

            time.sleep(2)
        
        except:
            next_chapter_available = False
        
    wattpad_story = {
        "story_title": story_title,
        "story_url": url,
        "reads": reads,
        "votes": votes,
        "chapters": wattpad_story_chapters
    }

    print("Finished reading story")
    
    return wattpad_story




""" 
    this function will determine in which file to save the following stories; if the last file created has less than 16 stories, add the following stories to it until it exceeds its limit,
    if not, create a new file with the next available number
"""
def determine_next_file_number():
    flag = "old_folder"
    if len(os.path.join("wattpad_scrapping" , "output"))==0:
        return 1
    
    highest_number = 1
    for file in os.listdir(os.path.join("wattpad_scrapping" , "output")):
        file_number = re.search("\d+", file).group()
        if int(file_number)>=highest_number:
            highest_number = int(file_number)
            
    with open(os.path.join("wattpad_scrapping" , "output", f"wattpad_stories_{highest_number}.json"), "r") as infile:
        if len(json.load(infile))==16:
            highest_number+=1
            flag = "new_folder"
            
    return highest_number, flag




"""
    This function parses the links from the "links_that_need_to_be_parsed.json", extracts the content from each link(story) and moves the link 
    to the "parsed_links.json" file, in order to mark it as a parsed link that does not need to be checked in the future.
    The stories' content will be saved inside a json file, and the maximum stories that will be saved to a single file will be 16.
"""
def extract_stories_wrapper(driver):
    
    with open(os.path.join(current_path , "utils", "links_that_need_to_be_parsed.json"), "r") as infile:
        links = json.load(infile)
        
    with open(os.path.join(current_path , "utils", "parsed_links.json"), "r") as infile:
        parsed_links = json.load(infile)
        
    file_number, flag = determine_next_file_number()
    if flag == "old_folder":
        with open(os.path.join("wattpad_scrapping" , "output", f"wattpad_stories_{file_number}.json"), "r") as infile:
            wattpad_stories_chunk = json.load(infile)
    elif flag == "new_folder":
        wattpad_stories_chunk = []
    
    while(len(links)>0):
        
        url = links.pop(0)
        wattpad_story = extract_story_content(driver, url)
        wattpad_stories_chunk.append(wattpad_story)
        parsed_links.append(url)
        
        with open(os.path.join("wattpad_scrapping" , "output", f"wattpad_stories_{file_number}.json"), "w") as outfile:
                outfile.write(json.dumps(wattpad_stories_chunk))
                
        with open(os.path.join(current_path , "utils", "parsed_links.json"), "w") as outfile:
                outfile.write(json.dumps(parsed_links))
                
        with open(os.path.join(current_path , "utils", "links_that_need_to_be_parsed.json"), "w") as outfile:
                outfile.write(json.dumps(links))
        
        # save a chunk of 16 stories in each json file
        if len(wattpad_stories_chunk)==16:

            wattpad_stories_chunk = []
                
            file_number+=1