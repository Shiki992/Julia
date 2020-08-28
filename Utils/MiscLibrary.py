'''
Library for Misc Functions utilised by bot
'''

# Imports
import webbrowser
import requests

# Main Functions
# ---------------------------------------- Stack Overflow Functions ---------------------------------------------------
def StackOverflow_SearchQuery(query):
    # Search stackoverflow(through api) for exact value of query and return json file
    resp = requests.get("https://api.stackexchange.com/" + "/2.2/search?order=desc&sort=activity&intitle={}&site=stackoverflow".format(query))
    return resp.json()

def GetAnswerURLs(results_json):
    # Read json file and get the urls of answers to query
    urls = []
    max_results = 3     # limit no of max results to 3
    
    result_count = 0
    for i in results_json["items"]:
        if (i["is_answered"]):
            urls.append(i["link"])
            print(i["link"])
            result_count += 1
        if result_count == max_results or result_count == len(i):
            break
    return urls

def OpenURLs(url_list):
    # Open Query URLs in web browser
    if len(url_list) == 0:
        print("Rejection is a part of life don't be sad")
        return
    for i in url_list:
        webbrowser.open(i)
# ---------------------------------------- Stack Overflow Functions ---------------------------------------------------