import spacy
from story_rewriter import Rewriter
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def take_screenshot(url, output_path="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url, timeout=60000)
        html_content = page.content()
        if not html_content:
            page.screenshot(path=output_path, full_page=True)
            print(f"Screenshot saved at: {output_path}")
        else:
            get_story(html_content)
        page.close()
        browser.close()

def get_story(html_content):
    bs = BeautifulSoup(html_content, 'html.parser')
    story_div = bs.find('div', class_="mw-parser-output")
    if not story_div:
        print("No content found in the specified div.")
        return None
    paras = story_div.find_all('p')
    with open("chapter_content.txt", "w", encoding="utf-8") as file:
        for para in paras:
            file.write(para.get_text(strip=True) + " ")
    print("Content extracted and saved to chapter_content.txt")

def rewrite_story(chapter_content_file="chapter_content.txt"):
    rewriter = Rewriter()
    with open(chapter_content_file, "r", encoding="utf-8") as file:
        story = file.read()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(story)
    sentences = [sent.text for sent in doc.sents]

    for i in range(0, len(sentences), 10):
        chunk = " ".join(sentences[i:i+10])
        rewritten_chunk = rewriter.rewrite(chunk).split('Text:')[1].strip()
        print(rewritten_chunk, end = "")


if __name__ == "__main__":

    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1" # example url
    html_content = take_screenshot(chapter_url)
    rewrite_story()