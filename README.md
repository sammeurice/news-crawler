# Battery News Summarizer
This tool automatically visits a list of websites you provide, reads the content, and uses Artificial Intelligence (ChatGPT) to generate a summary of the latest news.

## 1. Prerequisites (Before you start)
To run this tool, you will need a "Secret Key" from two services. These keys act like passwords that allow the script to access the AI tools.

* **OpenAI API Key:** You can get this from platform.openai.com.

* **Firecrawl API Key:** You can get this from the Firecrawl website.

## 2. Installation
### Step A: Create a Virtual Environment
This creates a localized folder for the project so it doesn't interfere with other things on your computer.

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### Step B: Install Required Libraries
Once your environment is active (you should see (venv) in your terminal line), run the following command to install the necessary tools:

```bash
pip install openai python-dotenv firecrawl-py jinja2
```

## 3. Configuration
### Setting up the .env file (API Keys)
The code looks for your passwords in a hidden file named .env. This ensures you don't accidentally share your passwords if you send the code to someone else.

* 1. Create a new file in this folder named exactly .env (the dot is important).

* 2. Open it with a text editor and paste the following, replacing the text after the = with your actual keys:

```Plaintext
OPENAI_API_KEY=sk-proj-your-openai-key-here
FIRECRAWL_API_KEY=fc-your-firecrawl-key-here
```

### Modifying sites.csv (Websites to crawl)
The project includes a file named sites.csv. This file acts as the list of instructions for the crawler. You can open this file in Excel or any text editor to change which websites are read.

The file has two columns:

* **url:** The website address you want to read.

* **limit:** A number representing how deep to crawl (how many "sub-pages" to visit).

To add a new site, simply add a new line to the bottom of the file.

### Example:

```Code snippet
url,limit
https://www.batterynews.com,5
https://www.technews.example.com/batteries,3
```

### Customizing the AI's Summary Instructions
The instructions for how the AI should summarize the news are now in a dedicated file, making them easy to change.

**The file to edit is:** `llm_template.txt`

You can open this plain text file and change the rules for the AI.

**What you can change:**

* **The Main Instructions:** You can freely change the text that tells the AI what its job is (e.g., changing "expert news summarization assistant" to "creative marketing copywriter").

* **The Bullet Points:** You can modify, add, or remove the bullet points under the INSTRUCTIONS section. This is how you control the length, tone, and focus of the final summary.

**What you should NOT change:**

* **Special Keywords (Placeholders):** Do not change any text inside double curly brackets, like `{{ articles }}` or `{{ max_length_words }}`. These are special keywords that the script uses to insert the news content and other data. Changing these will break the tool.

## 4. How to Run It (Normal vs. Test Mode)
There are two ways to run this tool depending on what you want to do.

**Option A: The "Live" Run (Get Fresh News)**
Use this mode when you want to fetch the absolute latest news from the internet. This takes longer because it has to visit every website.

**Command:**

```bash
python3 main.py
```

* **What happens:** It scrapes the websites, saves the articles to a local file (articles_cache.json), and prints the summary.

* **Note:** This takes a few minutes with just 1 site because of the scraping. I haven't tested this thoroughly but I imagine with lots of sites this will take a while.

**Option B: The "Test" Run (Fast Mode)**
Use this mode when you are editing `llm_template.txt` and want to see how your changes look immediately. It skips the slow website scraping and re-uses the news from your last "Live" run.

**Command:**

```bash
python3 main.py --test
```
* **What happens:** It instantly loads the saved articles and prints a new summary based on your updated instructions.

* **Note:** You must run Option A at least once before you can use Option B.

## 5. Understanding the Output
Currently, the script will print the final summary directly to your Console/Terminal window.

* Note: The tool does not save the summary to a file automatically. If you want to save the text, you can copy and paste it from the terminal, or the code can be modified later to save a .txt file.



## Troubleshooting / Notes for Developers
* **Dependencies:** The script relies on openai, python-dotenv, jinja2, and firecrawl.

* **Crawl Depth:** Be careful setting the limit in the CSV too high (e.g., 50+), as this will consume more API credits and take significantly longer to run.
