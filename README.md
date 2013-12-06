Use the Google Custom Search API to search the web from Python.

**This is by no means a finished library!**

# Quick start

```python

from google_search import GoogleCustomSearch


SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']                           
API_KEY = os.environ['GOOGLE_CLOUD_API_KEY']

api = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)

for result in api.search('pdf', 'http://scraperwiki.com'):
    print(result['title']) 
    print(result['link']) 
    print(result['snippet']) 
```

See these instructions (although the process wasn't completely the same):

http://stackoverflow.com/a/11206266


# 1. Make a Google Custom Search Engine

- Go to https://www.google.com/cse/

- It has a search engine ID

- Note the Safesearch setting in "Search features" => "Advanced"
  => "Websearch Settings"

- You can test the custom search engine by directly visiting its "Public URL"
  which is found in "Setup" => "Details" => "Public URL"

- There's a horrible hard limit of 10 sites before it uses a reduced index,
  see this: https://support.google.com/customsearch/answer/70392?hl=en

- "By the way, you can only ever get 64 results from any search using the AJAX
  API, and with the free Custom Search Engine, can only do 100 searches per
  day.  If you upgrade to the Site Search Engine, you can use the XML API and I
  believe you can get more results per search."
  http://productforums.google.com/forum/#!topic/customsearch/zqrQ3ISCiGA

# 2. Make a Google Cloud Console "Project" to get API key

- Provides an API key - explained in the developer docs at
  https://developers.google.com/custom-search/json-api/v1/overview

- You need to enable access to Custom Search service

- Allows separating billing for different projects, using the same custom
  search engine.

- To view your quota, go to "APIs & auth" => "APIs" => "Custom Search API"
  => "Quota" at the top.

When you make a Cloud Project, you need to enable the "Custom Search API"
feature.


To get an API key, go to "APIs & Auth" => Registered apps => Register New App
=> Web Application => Server Key

# Limitations

If you try and search across more than 10 sites (including "the whole web")
you'll get results from a limited subset of the Google Index:

[https://support.google.com/customsearch/answer/70392?hl=en](https://support.google.com/customsearch/answer/70392?hl=en)

"""If your custom search engine includes more than ten sites, the results may
be from a subset of our index and may differ from the results of a 'site:'
search on Google.com."""
