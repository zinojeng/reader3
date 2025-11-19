# reader 3

![reader3](reader3.png)

A lightweight, self-hosted document reader that lets you read through EPUB books, PDF documents, and Markdown files one section at a time. This makes it very easy to copy paste contents to an LLM, to read along. Get documents from various sources, open them up in this reader, copy paste text around to your favorite LLM, and read together and along.

## Features

- **Multiple Format Support**: Upload and read EPUB, PDF, and Markdown (.md) files
- **User-Friendly Streamlit UI**: Upload and process documents directly through a modern web interface
- **AI Model Integration**: Support for both OpenAI (GPT-5, GPT-4) and Google Gemini (Gemini 3, 2.5, 2.0) models
- **API Key Management**: Separate API key inputs for OpenAI and Gemini with secure storage
- **Section-by-Section Reading**: Clean, distraction-free reading experience optimized for LLM integration
- **Library Management**: Automatically manages your document collection
- **FastAPI Alternative**: Classic web server option still available for EPUB files

## Usage

The project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Option 1: Streamlit UI (Recommended)

The easiest way to use Reader3 is with the Streamlit interface:

```bash
uv run streamlit run app.py
```

This will open a user-friendly web interface where you can:
1. **Choose AI Provider**: Select between OpenAI or Google Gemini
2. **Configure API Key**: Enter your API key for the selected provider
3. **Select Model**: Choose from latest models (GPT-5, Gemini 3, etc.)
4. **Upload Documents**: Support for EPUB, PDF, and Markdown files
5. **Browse Library**: View all processed documents
6. **Read**: Navigate sections with Previous/Next buttons

The app will automatically open in your default browser at `http://localhost:8501`

### Option 2: Command Line + FastAPI Server

For the original CLI workflow, download an EPUB (e.g., [Dracula EPUB3](https://www.gutenberg.org/ebooks/345)) and process it:

```bash
uv run reader3.py dracula.epub
```

This creates the directory `dracula_data`, which registers the book to your local library. Then run the server:

```bash
uv run server.py
```

And visit [localhost:8123](http://localhost:8123/) to see your Library.

## Supported Document Formats

### EPUB Books
Find free, legal EPUB books at:
- [Project Gutenberg](https://www.gutenberg.org/) - Classic literature
- [Standard Ebooks](https://standardebooks.org/) - High-quality public domain books
- [Open Library](https://openlibrary.org/) - Internet Archive's digital library

### PDF Documents
- Research papers and academic articles
- Technical documentation
- eBooks in PDF format
- Any PDF document you want to read

### Markdown Files
- Technical documentation
- README files
- Notes and guides
- Blog posts
- Any .md or .markdown files

**Processing Details:**
- **EPUB**: Preserves structure, TOC, and images
- **PDF**: Groups every 10 pages into sections for easy navigation
- **Markdown**: Automatically splits by headers (H1/H2) into chapters with syntax highlighting

## Library Management

Books are stored as processed data in folders ending with `_data`. You can:
- Delete a book by removing its `*_data` folder
- Back up books by copying their folders
- Share books by copying the processed folders to another machine

## Deployment to Zeabur

Reader3 can be easily deployed to [Zeabur](https://zeabur.com) for cloud hosting:

### Quick Deploy

1. **Fork or Clone** this repository to your GitHub account

2. **Connect to Zeabur**:
   - Go to [Zeabur Dashboard](https://dash.zeabur.com)
   - Create a new project
   - Click "Deploy New Service" → "GitHub"
   - Select this repository

3. **Configure Environment** (Optional):
   - Add environment variables for API keys if needed
   - Zeabur will automatically detect the Streamlit app

4. **Deploy**:
   - Zeabur will automatically build and deploy using the provided configuration
   - Your app will be live at `your-project.zeabur.app`

### Deployment Files

The following files are configured for Zeabur deployment:
- `zbpack.json` - Zeabur build and start commands
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `.streamlit/config.toml` - Streamlit server configuration

**Note**: The main file is `app.py` (no need to rename for Zeabur deployment).

### After Deployment

Once deployed, users can:
- Access the app via the provided Zeabur URL
- Upload EPUB files (stored temporarily during the session)
- Configure their own API keys for OpenAI or Gemini
- Read books with the full feature set

## License

MIT