import argparse
import csv
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from firecrawl import Firecrawl
from jinja2 import Environment, FileSystemLoader

# Load environment variables from .env file
load_dotenv()
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

# Set up argument parser for article caching
CACHE_FILE = "articles_cache.json"

parser = argparse.ArgumentParser(description="Battery News Summarizer")
parser.add_argument("--test", action="store_true", help="Skip scraping and use cached articles")
args = parser.parse_args()

# Get sites to crawl from sites.csv. Return a dict containing the url of the site and it's crawl limit.
def get_sites():
    print("Getting sites...")
    sites = []

    with open('sites.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            url = row['url']
            limit = int(row['limit']) 
            
            sites.append({'url': url, 'limit': limit})
            

    print(f"Got {str(len(sites))} sites")
    return sites

# Given a crawled page, return all the data found joined into one string.
def get_markdown_from_article(article):
    markdown = ""
    for element in article.data:
        markdown += element.markdown

    return markdown

# Given a list of sites, return a list of articles.
def get_articles(sites):
    # Test mode
    if args.test:
        print("TEST MODE: Attempting to read articles from cache... ")
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                articles = json.load(f)
            print(f"Loaded {len(articles)} articles from {CACHE_FILE}")
            return articles
        else:
            print(f"Error: No cache file found at {CACHE_FILE}. Run without --test first to generate one.")
            return

    # Live mode
    print("LIVE MODE: Scraping websites... ")
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

    print(f"Scraped {len(articles)} articles")

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)
        print(f"Saved scraped articles to {CACHE_FILE}")

    return articles


# Given a list of articles as strings, generate a prompt to give to ChatGPT to summarize them.
def create_prompt(articles):
    llm_context = {
        "num_articles": len(articles),
        "articles": "\n---\n".join(articles)
    }
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    template = env.get_template('llm_template.txt')
    final_prompt = template.render(llm_context)

    return final_prompt

def call_chat(prompt):
    print("Sending prompt to LLM... ")
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
