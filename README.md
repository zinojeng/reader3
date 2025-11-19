# reader 3

![reader3](reader3.png)

A lightweight, self-hosted EPUB reader that lets you read through EPUB books one chapter at a time. This makes it very easy to copy paste the contents of a chapter to an LLM, to read along. Basically - get epub books (e.g. [Project Gutenberg](https://www.gutenberg.org/) has many), open them up in this reader, copy paste text around to your favorite LLM, and read together and along.

## Features

- **User-Friendly Streamlit UI**: Upload and process EPUB files directly through a modern web interface
- **API Key Management**: Optional OpenAI API key input for future AI-powered features
- **Chapter-by-Chapter Reading**: Clean, distraction-free reading experience optimized for LLM integration
- **Library Management**: Automatically manages your book collection
- **FastAPI Alternative**: Classic web server option still available

## Usage

The project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Option 1: Streamlit UI (Recommended)

The easiest way to use Reader3 is with the Streamlit interface:

```bash
uv run streamlit run app.py
```

This will open a user-friendly web interface where you can:
1. Upload EPUB files directly through your browser
2. (Optional) Add your OpenAI API key for future AI features
3. Browse your library and read books
4. Navigate chapters with Previous/Next buttons

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

## Finding EPUB Books

You can find free, legal EPUB books at:
- [Project Gutenberg](https://www.gutenberg.org/) - Classic literature
- [Standard Ebooks](https://standardebooks.org/) - High-quality public domain books
- [Open Library](https://openlibrary.org/) - Internet Archive's digital library

## Library Management

Books are stored as processed data in folders ending with `_data`. You can:
- Delete a book by removing its `*_data` folder
- Back up books by copying their folders
- Share books by copying the processed folders to another machine

## License

MIT