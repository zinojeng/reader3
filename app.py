"""
Streamlit-based UI for Reader3 EPUB reader
Provides a user-friendly interface for uploading EPUBs and reading books
"""

import os
import streamlit as st
from pathlib import Path
import tempfile
from reader3 import process_epub, save_to_pickle, Book
import pickle
from typing import Optional

# Page config
st.set_page_config(
    page_title="Reader3 - EPUB Reader",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better reading experience
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .book-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    .book-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .book-meta {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .chapter-content {
        font-family: Georgia, serif;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: justify;
        max-width: 800px;
        margin: 0 auto;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Directory setup
BOOKS_DIR = Path(".")

def load_book_from_folder(folder_name: str) -> Optional[Book]:
    """Load a book from its pickle file"""
    file_path = BOOKS_DIR / folder_name / "book.pkl"
    if not file_path.exists():
        return None

    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading book {folder_name}: {e}")
        return None

def get_all_books():
    """Scan directory for processed books"""
    books = []
    if BOOKS_DIR.exists():
        for item in BOOKS_DIR.iterdir():
            if item.is_dir() and item.name.endswith("_data"):
                book = load_book_from_folder(item.name)
                if book:
                    books.append({
                        "id": item.name,
                        "title": book.metadata.title,
                        "authors": book.metadata.authors,
                        "chapters": len(book.spine),
                        "book": book
                    })
    return books

def process_uploaded_epub(uploaded_file):
    """Process an uploaded EPUB file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        # Generate output directory name
        base_name = Path(uploaded_file.name).stem
        output_dir = str(BOOKS_DIR / f"{base_name}_data")

        # Process the EPUB
        with st.spinner(f"Processing {uploaded_file.name}..."):
            book = process_epub(tmp_path, output_dir)
            save_to_pickle(book, output_dir)

        return book, output_dir
    finally:
        # Clean up temp file
        os.unlink(tmp_path)

def display_chapter(book: Book, chapter_index: int):
    """Display a chapter with navigation"""
    if chapter_index < 0 or chapter_index >= len(book.spine):
        st.error("Chapter not found")
        return

    current_chapter = book.spine[chapter_index]

    # Chapter navigation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if chapter_index > 0:
            if st.button("← Previous"):
                st.session_state.current_chapter = chapter_index - 1
                st.rerun()
        else:
            st.button("← Previous", disabled=True)

    with col2:
        st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>Section {chapter_index + 1} of {len(book.spine)}</div>",
                   unsafe_allow_html=True)

    with col3:
        if chapter_index < len(book.spine) - 1:
            if st.button("Next →"):
                st.session_state.current_chapter = chapter_index + 1
                st.rerun()
        else:
            st.button("Next →", disabled=True)

    st.divider()

    # Display chapter content
    st.markdown(f'<div class="chapter-content">{current_chapter.content}</div>',
               unsafe_allow_html=True)

    st.divider()

    # Bottom navigation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if chapter_index > 0:
            if st.button("← Previous", key="prev_bottom"):
                st.session_state.current_chapter = chapter_index - 1
                st.rerun()

    with col3:
        if chapter_index < len(book.spine) - 1:
            if st.button("Next →", key="next_bottom"):
                st.session_state.current_chapter = chapter_index + 1
                st.rerun()

# Model configurations
OPENAI_MODELS = {
    "GPT-5.1 (Reasoning + Agentic)": "gpt-5.1",
    "GPT-5 Mini": "gpt-5-mini",
    "GPT-5 Nano": "gpt-5-nano",
    "GPT-4.1": "gpt-4.1",
    "GPT-4.1 Mini": "gpt-4.1-mini",
    "GPT-4.1 Nano": "gpt-4.1-nano",
    "GPT-4o": "gpt-4o",
    "GPT-4o Mini": "gpt-4o-mini",
    "o3 (Reasoning)": "o3",
    "o4-mini (Reasoning)": "o4-mini",
    "o4-mini-high (Reasoning)": "o4-mini-high",
}

GEMINI_MODELS = {
    "Gemini 3 Pro (Preview)": "gemini-3-pro-preview",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Flash-Lite": "gemini-2.5-flash-lite",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite",
}

# Initialize session state
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'ai_provider' not in st.session_state:
    st.session_state.ai_provider = "OpenAI"
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = ""
if 'current_book' not in st.session_state:
    st.session_state.current_book = None
if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = 0
if 'view' not in st.session_state:
    st.session_state.view = "library"

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Reader3")
    st.markdown("---")

    # AI Model Configuration
    st.markdown("#### 🤖 AI Model Settings")

    # Provider selection
    provider = st.selectbox(
        "AI Provider",
        ["OpenAI", "Google Gemini"],
        index=0 if st.session_state.ai_provider == "OpenAI" else 1,
        help="Choose your AI provider for enhanced features"
    )
    st.session_state.ai_provider = provider

    # API Key input based on provider
    if provider == "OpenAI":
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.openai_api_key,
            help="Enter your OpenAI API key for AI-powered features"
        )
        if openai_key:
            st.session_state.openai_api_key = openai_key
            st.success("✓ OpenAI API key configured")

        # Model selection
        model_display_names = list(OPENAI_MODELS.keys())
        selected_model_display = st.selectbox(
            "Select Model",
            model_display_names,
            help="Choose the OpenAI model to use"
        )
        st.session_state.selected_model = OPENAI_MODELS[selected_model_display]

        # Model info
        with st.expander("ℹ️ Model Information"):
            st.markdown("""
            **GPT-5 Family** (Latest): Best for coding and agentic tasks
            - GPT-5.1: Top model with configurable reasoning effort for complex tasks
            - GPT-5 Mini: Faster, cost-efficient for well-defined tasks
            - GPT-5 Nano: Fastest, most cost-efficient version

            **GPT-4.1 Family**: Improved coding and instruction following
            - GPT-4.1: Full-featured flagship model
            - GPT-4.1 Mini: Faster, cost-effective version
            - GPT-4.1 Nano: Ultra-fast, budget-friendly

            **GPT-4o Family**: Multimodal models with native vision
            - GPT-4o: Versatile omni-model
            - GPT-4o Mini: Quick and economical

            **O-Series**: Advanced reasoning models
            - Specialized for complex problem-solving
            - Strong in science, coding, and math
            """)

    else:  # Google Gemini
        gemini_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=st.session_state.gemini_api_key,
            help="Enter your Google Gemini API key"
        )
        if gemini_key:
            st.session_state.gemini_api_key = gemini_key
            st.success("✓ Gemini API key configured")

        # Model selection
        model_display_names = list(GEMINI_MODELS.keys())
        selected_model_display = st.selectbox(
            "Select Model",
            model_display_names,
            help="Choose the Gemini model to use"
        )
        st.session_state.selected_model = GEMINI_MODELS[selected_model_display]

        # Model info
        with st.expander("ℹ️ Model Information"):
            st.markdown("""
            **Gemini 3 Pro (Preview)**: Latest flagship model
            - 1M token input / 64k token output
            - Advanced reasoning with dynamic thinking
            - Knowledge cutoff: January 2025
            - Supports tools: Google Search, Code Execution
            - Best for complex tasks requiring broad world knowledge

            **Gemini 2.5 Family**: State-of-the-art performance
            - Pro: Top thinking model
            - Flash: Best price-performance
            - Flash-Lite: Ultra-fast and cost-efficient

            **Gemini 2.0 Family**: Second-gen workhorse
            - Flash: Balanced performance
            - Flash-Lite: Lightweight variant

            All models support text, image, video, audio, and PDF inputs
            """)

    # Display current configuration
    if st.session_state.selected_model:
        st.info(f"🎯 Current: {provider} - {selected_model_display}")

    st.markdown("---")

    # Upload EPUB
    st.markdown("#### Upload EPUB")
    uploaded_file = st.file_uploader("Choose an EPUB file", type=['epub'])

    if uploaded_file:
        if st.button("Process Book"):
            try:
                book, output_dir = process_uploaded_epub(uploaded_file)
                st.success(f"✓ Successfully processed: {book.metadata.title}")
                st.info(f"Book saved to: {output_dir}")
                # Refresh the view
                st.session_state.view = "library"
                st.rerun()
            except Exception as e:
                st.error(f"Error processing EPUB: {e}")

    st.markdown("---")

    # Navigation
    if st.button("🏠 Library"):
        st.session_state.view = "library"
        st.session_state.current_book = None
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    Reader3 is a lightweight EPUB reader designed for reading books alongside LLMs.

    Upload EPUB files, process them, and read chapter by chapter with easy copy-paste functionality.
    """)

# Main content area
if st.session_state.view == "library":
    st.markdown('<div class="main-header">📖 My Library</div>', unsafe_allow_html=True)

    books = get_all_books()

    if not books:
        st.info("No books in your library yet. Upload an EPUB file to get started!")
        st.markdown("""
        ### Getting Started
        1. Upload an EPUB file using the sidebar
        2. Click 'Process Book' to add it to your library
        3. Start reading!

        You can find free EPUB books at [Project Gutenberg](https://www.gutenberg.org/)
        """)
    else:
        # Display books in a grid
        cols_per_row = 2
        for i in range(0, len(books), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(books):
                    book_data = books[i + j]
                    with col:
                        with st.container():
                            st.markdown(f"""
                            <div class="book-card">
                                <div class="book-title">{book_data['title']}</div>
                                <div class="book-meta">
                                    {', '.join(book_data['authors']) if book_data['authors'] else 'Unknown Author'}<br>
                                    {book_data['chapters']} sections
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            if st.button(f"Read Book", key=f"read_{book_data['id']}"):
                                st.session_state.current_book = book_data['id']
                                st.session_state.current_chapter = 0
                                st.session_state.view = "reader"
                                st.rerun()

elif st.session_state.view == "reader" and st.session_state.current_book:
    book = load_book_from_folder(st.session_state.current_book)

    if book:
        # Book header
        st.markdown(f'<div class="main-header">{book.metadata.title}</div>', unsafe_allow_html=True)
        if book.metadata.authors:
            st.markdown(f"*by {', '.join(book.metadata.authors)}*")

        st.divider()

        # Table of contents in sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown("#### Table of Contents")

            def render_toc(items, depth=0):
                for item in items:
                    # Find matching spine index
                    spine_idx = None
                    for i, ch in enumerate(book.spine):
                        if ch.href == item.file_href:
                            spine_idx = i
                            break

                    indent = "&nbsp;" * (depth * 4)
                    if spine_idx is not None:
                        if st.button(f"{item.title}", key=f"toc_{item.href}_{depth}"):
                            st.session_state.current_chapter = spine_idx
                            st.rerun()
                    else:
                        st.markdown(f"{indent}{item.title}")

                    if item.children:
                        render_toc(item.children, depth + 1)

            render_toc(book.toc)

        # Display current chapter
        display_chapter(book, st.session_state.current_chapter)
    else:
        st.error("Could not load book")
        if st.button("Return to Library"):
            st.session_state.view = "library"
            st.rerun()
