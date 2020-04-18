#This code is a development of the code found at
#https://www.textjuicer.com/2019/07/crawling-all-submissions-from-a-subreddit/

import requests
import time
import pandas as pd

url = "https://api.pushshift.io/reddit/search/submission"

def crawl_page(subreddit: str, sort_by: str, last_page = None):
  
  params = {"subreddit": subreddit, "size": 500, "sort": "desc", "sort_type": sort_by}
  if last_page is not None:
    if len(last_page) > 0:
      # resume from where we left at the last page
      params["before"] = last_page[-1][sort_by]
    else:
      # the last page was empty, we are past the last page
      return []
  results = requests.get(url, params)
  if not results.ok:
    # something wrong happened
    raise Exception("Server returned status code {}".format(results.status_code))
  return results.json()["data"]

def crawl_subreddit(subreddit, sort_by, max_submissions = 2000):
  
  submissions = []
  last_page = None
  while last_page != [] and len(submissions) < max_submissions:
    last_page = crawl_page(subreddit, sort_by, last_page)
    submissions += last_page
    print(str(len(submissions)) + str(" posts obtained out of ") + str(max_submissions))
    time.sleep(2)
  return submissions[:max_submissions]


latest_submissions = crawl_subreddit("coronavirusDownunder", "created_utc")


df = pd.DataFrame(latest_submissions)


df.to_csv("/dataset/CoronavirusDownunder.csv", index = False)
