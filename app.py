import streamlit as st
import os

from utils.file_loader import process_file
from utils.text_processor import process_text, create_chunks
from utils.summarizer import generate_summary
from utils.extractor import extract_information
from utils.vector_store import store_in_chroma
from utils.rag_pipeline import ask_question

st.set_page_config(
    page_title="Document AI System",
    layout="wide"
)

st.title("📄 AI Document Summarizer & Extractor")

# =========================
# FILE UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload documents",
    accept_multiple_files=True,
    type=["pdf", "txt", "docx", "png", "jpg", "jpeg"]
)

# =========================
# PROCESS BUTTON
# =========================

if uploaded_files:

    process_button = st.button("🚀 Process Documents")

    if process_button:

        os.makedirs("uploads", exist_ok=True)

        all_processed_text = ""

        for uploaded_file in uploaded_files:

            # Save uploaded file
            file_path = os.path.join(
                "uploads",
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Uploaded: {uploaded_file.name}")

            # Extract text
            extracted_text = process_file(file_path)

            # Process text
            processed_text = process_text(extracted_text)

            # Combine all documents
            all_processed_text += processed_text + "\n\n"

        # Create chunks
        chunks = create_chunks(all_processed_text)

        # Store embeddings
        vector_db = store_in_chroma(chunks)

        # Generate summary
        with st.spinner("Generating AI Summary..."):

            summary = generate_summary(all_processed_text)

        # Extract structured info
        with st.spinner("Extracting Important Information..."):

            extracted_info = extract_information(
                all_processed_text
            )

        # =========================
        # STORE EVERYTHING
        # =========================

        st.session_state.documents_processed = True

        st.session_state.processed_text = all_processed_text

        st.session_state.chunks = chunks

        st.session_state.summary = summary

        st.session_state.extracted_info = extracted_info

# =========================
# SHOW RESULTS
# =========================

if "documents_processed" in st.session_state:

    processed_text = st.session_state.processed_text
    chunks = st.session_state.chunks

    st.markdown("---")

    st.subheader("📊 Document Analytics")

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Characters",
            len(processed_text)
        )

    with col2:
        st.metric(
            "Words",
            len(processed_text.split())
        )

    with col3:
        st.metric(
            "Chunks",
            len(chunks)
        )

    st.success("✅ Embeddings stored successfully in ChromaDB")

    # =========================
    # TABS
    # =========================

    # tab1, tab2, tab3, tab4, tab5 = st.tabs([
        # "📘 Extracted Text",
        # "📝 Preview",
        # "🧩 Chunks",
        # "🤖 AI Summary",
        # "📊 Structured Data"
    # ])
    
    tab1, tab2, tab3  = st.tabs([
        "📝 Preview",
        "🤖 AI Summary",
        "📊 Structured Data"
    ])

    # =========================
    # TAB 1
    # =========================

    with tab1:

        st.text_area(
            "Document Content",
            processed_text,
            height=400
        )

    # =========================
    # TAB 2
    # =========================

    with tab2:

        st.markdown(processed_text)

    # =========================
    # TAB 3
    # =========================

    with tab3:

        st.write(f"Total Chunks: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            with st.expander(f"Chunk {i+1}"):

                st.write(chunk)

    # =========================
    # TAB 4
    # =========================

    with tab4:

        st.markdown(
            st.session_state.summary
        )

    # =========================
    # TAB 5
    # =========================

    with tab5:

        st.markdown(
            st.session_state.extracted_info
        )

    # =========================
    # RAG Q&A
    # =========================

    st.markdown("---")

    st.subheader("💬 Ask Questions From Documents")

    question = st.text_input(
        "Ask something about the uploaded documents"
    )

    if question:

        with st.spinner("Searching documents..."):

            answer = ask_question(question)

        st.markdown("### 🤖 Answer")

        st.write(answer)