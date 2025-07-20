# AI Story Writer - Human-in-the-Loop Story Rewriting System

## 📋 Project Overview

An AI-powered story rewriting system that fetches content from web URLs, applies AI-driven "spinning" to chapters, and enables multiple human-in-the-loop iterations for continuous model improvement.

## 🎯 Key Features

### 1. **Web Content Fetching & Screenshots**
- Fetch content from URLs (e.g., Wikisource pages)
- Save screenshots of web pages using Playwright
- Extract and process text content for AI rewriting

### 2. **AI Writing & Review**
- Use LLMs (TinyLlama) for chapter "spinning" (rewriting with variation)
- Customizable AI prompts for different rewriting styles
- Batch processing of story chunks for optimal performance

### 3. **Human-in-the-Loop Workflow**
- Interactive web interface for story processing
- Editable AI-rewritten content for human refinement
- Submit edits for model fine-tuning and style adaptation
- Multiple iteration support (Writer → Reviewer → Editor)

### 4. **Reinforcement Learning Integration**
- Change-based reward system for model improvement
- Collect human edits as training data
- Prepare for RL-based inference and model fine-tuning

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI/ML**: TinyLlama, Transformers (HuggingFace)
- **Web Scraping**: Playwright, BeautifulSoup
- **Data Processing**: Python, JSON
- **Version Control**: Git

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd storyWritter
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn playwright beautifulsoup4 transformers torch jinja2 python-multipart
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Set up environment (Windows)**
   ```python
   # Add this at the top of app.py for Windows compatibility
   import sys
   import asyncio
   if sys.platform.startswith('win'):
       asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
   ```

## 🚀 Usage

### Starting the Application

1. **Run the FastAPI server**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the web interface**
   - Open your browser and go to `http://localhost:8000`
   - You'll see the AI Story Spinner interface

### Using the Application

1. **Process a Story from URL**
   - Enter a URL (e.g., `https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1`)
   - Optionally enter a custom AI prompt for rewriting
   - Click "Process Story"

2. **Review and Edit**
   - View the original story and AI-rewritten version side by side
   - Edit the rewritten story directly in the textarea
   - Click "Submit Edit" to save your changes

3. **Model Learning**
   - Your edits are collected for model fine-tuning
   - The system learns from your writing style preferences
   - Future AI outputs will adapt to your editing patterns

## 📁 Project Structure

```
storyWritter/
├── app.py                 # Main FastAPI application
├── get_data.py           # Web scraping and content fetching
├── story_rewriter.py     # AI model and rewriting logic
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling for the web interface
│   └── js/
│       └── main.js       # Frontend JavaScript logic
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## 🔧 API Endpoints

### `GET /`
- Renders the main web interface

### `POST /process_url`
- **Parameters**: `url` (string), `prompt` (string, optional)
- **Returns**: JSON with original and rewritten content
- **Purpose**: Fetch and rewrite story content

### `POST /submit_edit`
- **Parameters**: `original` (string), `rewritten` (string), `edited` (string)
- **Returns**: JSON confirmation message
- **Purpose**: Save human edits for model training

## 🤖 AI Model Details

### Current Model
- **Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Type**: Instruction-tuned language model
- **Purpose**: Story rewriting and style adaptation

### Prompt Format
```
[INST]
You are a professional story writer known for your rich third-person narration style.
Rewrite the following passage from a strong third-person narrative perspective.
Enhance the flow, add vivid descriptions, and make the emotions and actions more immersive.
Keep the events and character dialogue faithful to the original.

Text:
{original_content}
[/INST]
```

## 🔄 Human-in-the-Loop Process

1. **Content Fetching**: Extract story from web URL
2. **AI Rewriting**: Apply AI model to rewrite content
3. **Human Review**: User reviews and edits AI output
4. **Edit Submission**: Save edits for model training
5. **Model Adaptation**: Use edits to improve future outputs

## 🎯 Future Enhancements

### Planned Features
- [ ] **RL-based Reward System**: Implement change-based reward calculation
- [ ] **Model Fine-tuning**: Automatic model updates based on human feedback
- [ ] **Agentic API**: Seamless content flow between AI agents

### RL Implementation Strategy
- **Change Detection**: Count character/word changes between AI output and human edits
- **Threshold-based Rewards**: Use edit volume as reward signal
- **Batch Fine-tuning**: Aggregate edits and retrain model periodically
- **Style Adaptation**: Learn user-specific writing preferences

## 🐛 Troubleshooting

### Common Issues

1. **Playwright Errors on Windows**
   - Ensure you've set the event loop policy in `app.py`
   - Install Playwright browsers: `playwright install`

2. **Model Loading Issues**
   - Check internet connection for model download
   - Ensure sufficient disk space for model files

3. **Memory Issues**
   - Reduce batch size in `story_rewriter.py`
   - Use smaller model variants if needed

## 📝 Development Notes

### Adding New Features
- **Frontend**: Modify `templates/index.html` and `static/js/main.js`
- **Backend**: Update `app.py` with new endpoints
- **AI Logic**: Extend `story_rewriter.py` for new capabilities
- **Data Fetching**: Enhance `get_data.py` for new sources

### Debugging
- Check console logs for detailed execution flow
- Use print statements throughout the codebase for debugging
- Monitor FastAPI logs for API endpoint issues
