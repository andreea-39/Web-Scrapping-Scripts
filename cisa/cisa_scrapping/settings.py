from fake_useragent import UserAgent


def init_user_agent():
    user_agent = UserAgent(browsers=["chrome"])
    return user_agent