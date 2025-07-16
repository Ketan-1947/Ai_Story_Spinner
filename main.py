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
            file.write(para.get_text(strip=True) + "\n\n")
    print("Content extracted and saved to chapter_content.txt")

if __name__ == "__main__":

    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_2" # example url
    html_content = take_screenshot(chapter_url)