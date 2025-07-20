from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from get_data import fetcher
from story_rewriter import Rewriter

rewriter = Rewriter()
fetch = fetcher()
app = FastAPI()

# Mount static files and templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    print("[INFO] GET / - Rendering homepage")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_url")
def process_url(url: str = Form(...), prompt: str = Form("")):
    print(f"[INFO] POST /process_url - Received URL: {url}")
    print(f"[INFO] POST /process_url - Received Prompt: {prompt}")
    """
    Process a URL and return the rewritten story.
    """
    try:
        print("[INFO] Fetching content from URL...")
        original_content = fetch_content_from_url(url)
        print(f"[INFO] Content fetched. Length: {len(original_content) if hasattr(original_content, '__len__') else 'unknown'}")
        print("[INFO] Rewriting story with AI...")
        rewritten_content = rewrite_story_with_ai(original_content, prompt)
        print("[INFO] Story rewritten successfully.")
        return JSONResponse({
            "success": True,
            "original_content": original_content,
            "rewritten_content": rewritten_content
        })
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=400)

@app.post("/submit_edit")
def submit_edit(
    original: str = Form(...),
    rewritten: str = Form(...),
    edited: str = Form(...)
):
    print("[INFO] POST /submit_edit - Manual edit submitted")
    print(f"[DEBUG] Original: {original[:100]}...")
    print(f"[DEBUG] Rewritten: {rewritten[:100]}...")
    print(f"[DEBUG] Edited: {edited[:100]}...")
    """
    Handle manual story edit submissions.
    """
    return {"message": "story submitted"}

def fetch_content_from_url(url: str):
    print(f"[INFO] fetch_content_from_url - Fetching from: {url}")
    try:
        print(type(url))
        result = fetch.fetch(url)
        print(f"[INFO] fetch_content_from_url - Fetch complete. Type: {type(result)}")
        if result is None:
            raise ValueError("Fetcher returned None. Check fetcher implementation and upstream errors.")
        return result
    except Exception as e:
        print(f"[ERROR] fetch_content_from_url - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    # raise NotImplementedError("fetch_content_from_url is not implemented.")

def rewrite_story_with_ai(original_content, prompt=""):
    print("[INFO] rewrite_story_with_ai - Starting rewrite process")
    print(f"[INFO] rewrite_story_with_ai - Using prompt: {prompt}")
    try:
        story = ""
        for i in range(0, len(original_content), 5):
            content = " ".join(original_content[i:i+5])
            print(f"[DEBUG] Rewriting chunk {i//5+1}: {content[:60]}...")
            rewritten_content = rewriter.rewrite(content, prompt=prompt) if prompt else rewriter.rewrite(content)
            print(f"[DEBUG] Rewritten chunk {i//5+1}: {rewritten_content[:60]}...")
            story += rewritten_content
        print("[INFO] rewrite_story_with_ai - Rewrite complete")
        return story
    except Exception as e:
        print(f"[ERROR] rewrite_story_with_ai - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    # raise NotImplementedError("rewrite_story_with_ai is not implemented.")
