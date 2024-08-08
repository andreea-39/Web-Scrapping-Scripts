from scrape.service import extract_new_advisory_links, extract_advisory_soup


def start_service(flag, user_agent):
    if flag == 1:
        extract_new_advisory_links(user_agent)
    elif flag == 2:
        extract_advisory_soup(user_agent)