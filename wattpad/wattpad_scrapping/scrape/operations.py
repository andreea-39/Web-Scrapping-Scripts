from scrape.service import extract_stories_wrapper, extract_links_by_tags


# flag = 1 -> extracting links
# flag = 2 -> extracting stories' content for the new links
def start_service(flag, driver, tags=[]):
    
    if flag == 1:
        extract_links_by_tags(driver, tags)
    elif flag == 2:
        extract_stories_wrapper(driver)