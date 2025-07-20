import spacy
import torch
from story_rewriter import Rewriter
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys
import asyncio

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

print('[INFO] get_data.py loaded')

class fetcher:
    def __init__(self):
        print('[INFO] fetcher instance created')
        self.rewriter = Rewriter()
    def take_screenshot(self, url, output_path="screenshot.png"):
        try:
            with sync_playwright() as p:
                print('launched brower')
                browser = p.chromium.launch(headless=True)

                print('opening page')
                page = browser.new_page()

                print(f"Navigating to url")
                page.goto(url, timeout=60000)

                print(f"Waiting for page to load")
                page.wait_for_load_state("networkidle")

                print(f"Taking screenshot")
                html_content = page.content()
                if not html_content:
                    page.screenshot(path=output_path, full_page=True)
                    print(f"Screenshot saved at: {output_path}")
                else:
                    story = self.get_story(html_content)
                    page.close()
                    browser.close()
                    return story
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
        

    def get_story(self, html_content):
        bs = BeautifulSoup(html_content, 'html.parser')
        story_div = bs.find('div', class_="mw-parser-output")
        if not story_div:
            print("No content found in the specified div.")
            return None
        paras = story_div.find_all('p')
        story = ""
        for para in paras:
            story += para.get_text(strip=True) + " "
        print("Content extracted successfully.")
        return story.strip()

    def fetch(self,url):
        print(f'[INFO] fetcher.fetch called with URL: {url}')
        story = self.take_screenshot(url)

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(story)
        sentences = [sent.text for sent in doc.sents]

        return sentences


# if __name__ == "__main__":

#     chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1" # example url
#     rewriter = story_rewriter()
#     rewriter.rewrite_story(chapter_url)