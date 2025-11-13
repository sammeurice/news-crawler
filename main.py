import os
import csv
from openai import OpenAI
from dotenv import load_dotenv
from firecrawl import Firecrawl

# Load environment variables from .env file
load_dotenv()
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")


# Get sites to crawl from sites.csv. Return a dict containing the url of the site and it's crawl limit.
def get_sites():
    print("Getting sites")
    sites = []

    with open('sites.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            url = row['url']
            limit = int(row['limit']) 
            
            sites.append({'url': url, 'limit': limit})
            

    print("Got " + str(len(sites)) + " sites")
    return sites

# Given a crawled page, return all the data found joined into one string.
def get_markdown_from_article(article):
    markdown = ""
    for element in article.data:
        markdown += element.markdown

    return markdown

# Given a list of sites, return a list of articles.
def get_articles(sites):
    print("Getting articles")
    firecrawl = Firecrawl(api_key=firecrawl_api_key)
    
    articles = []
    for site in sites:
        article = firecrawl.crawl(
            site['url'],
            limit=site['limit'],
            scrape_options={
                'formats': ['markdown'],
            },
        )
        markdown = get_markdown_from_article(article)
        articles.append(markdown)

    print("Got " + str(len(articles)) + " articles")
    return articles


# Given a list of articles as strings, generate a prompt to give to ChatGPT to summarize them.
def create_prompt(articles):
    print("Creating prompt")
    header = '''
    You are an expert at summarizing documents.
    You will receive a list of articles, find the most important ones and generate a summary of what's happening in battery news.
'''
    separator = "<ARTICLE>"

    return header + separator.join(articles)

def call_chat(prompt):
    print("Sending prompt to LLM")
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

sites = get_sites()
articles = get_articles(sites)
prompt = create_prompt(articles)
response = call_chat(prompt)

print(response)
