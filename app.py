import streamlit as st
import os

print("START APP")

from utils.file_loader import process_file
print("FILE LOADER LOADED")

from utils.text_processor import process_text, create_chunks
print("TEXT PROCESSOR LOADED")

from utils.summarizer import generate_summary
print("SUMMARIZER LOADED")

from utils.extractor import extract_information
print("EXTRACTOR LOADED")

from utils.vector_store import store_in_chroma
print("VECTOR STORE LOADED")

from utils.rag_pipeline import ask_question
print("RAG PIPELINE LOADED")

st.set_page_config(
    page_title="Document AI System",
    layout="wide"
)

with st.sidebar:

    st.markdown("# 📄 DocAI")

    st.markdown("---")

    st.markdown("""
    ### Features

    ✅ Document Summarization

    ✅ Information Extraction

    ✅ Semantic Search (RAG)

    ✅ AI Question Answering
    """)

    st.markdown("---")

    st.info("Built with Streamlit + LangChain + Groq")

st.markdown("""
<div style="
padding:25px;
border-radius:15px;
background:linear-gradient(
90deg,
#1e3a8a,
#2563eb
);
color:white;
">

<h1>📄 DocAI Assistant</h1>

<h4>
Upload documents, generate summaries,
extract information and chat with your files using AI.
</h4>

</div>
""", unsafe_allow_html=True)

# =========================
# FILE UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload documents",
    accept_multiple_files=True,
    type=["pdf", "txt", "docx", "png", "jpg", "jpeg"]
)

if not uploaded_files:

    keys_to_remove = [
        "documents_processed",
        "processed_text",
        "chunks",
        "summary",
        "extracted_info",
        "vector_db",
        "chat_history"
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)
        
# =========================
# PROCESS BUTTON
# =========================

if uploaded_files:

    process_button = st.button("🚀 Process Documents")

    if process_button:
        
        # Clear old data
        keys_to_remove = [
            "documents_processed",
            "processed_text",
            "chunks",
            "summary",
            "extracted_info",
            "chat_history",
            "vector_db"
        ]

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

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
        st.session_state.vector_db = vector_db

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

if (
    "documents_processed" in st.session_state
    and st.session_state.get("processed_text")
):

    processed_text = st.session_state.get("processed_text")
    summary = st.session_state.get("summary")
    chunks = st.session_state.get("chunks")
    extracted_info = st.session_state.get("extracted_info")
    
    if not processed_text:
        st.stop()   

    st.markdown("---")

    st.subheader("📊 Document Analytics")

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📄 Characters",
            f"{len(processed_text):,}"
        )

    with col2:
        st.metric(
            "📝 Words",
            f"{len(processed_text.split()):,}"
        )

    with col3:
        st.metric(
            "🧩 Chunks",
            len(chunks)
        )

    st.success("✅ Embeddings stored successfully in ChromaDB")
    
    st.info("""
    📌 Document processed successfully.

    You can now:
    - View summary
    - Extract information
    - Ask questions
    """)

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
    
    tab1, tab2, tab3 = st.tabs([
        "📄 Document Preview",
        "🤖 AI Summary",
        "📊 Extracted Information"
    ])

    # =========================
    # TAB 1
    # =========================

    # with tab0:

        # st.text_area(
            # "Document Content",
            # processed_text,
            # height=400
        # )

    # =========================
    # TAB 2
    # =========================

    with tab1:

        st.markdown(processed_text)

    # =========================
    # TAB 3
    # =========================

    # with tab0:

        # st.write(f"Total Chunks: {len(chunks)}")

        # for i, chunk in enumerate(chunks):

            # with st.expander(f"Chunk {i+1}"):

                # st.write(chunk)

    # =========================
    # TAB 4
    # =========================

    with tab2:

        st.markdown(
            st.session_state.summary
        )

    # =========================
    # TAB 5
    # =========================

    with tab3:

        st.markdown(
            st.session_state.extracted_info
        )

    # =========================
    # RAG Q&A
    # =========================

    st.markdown("---")

    st.subheader("💬 Ask Questions From Documents")

    # Create chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show old chats
    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

        st.markdown("---")

    # Chat input
    question = st.chat_input(
        "Ask something about the uploaded documents..."
    )

    if question:

        if "vector_db" not in st.session_state:
            st.warning("Please process a document first.")
            st.stop()

        with st.spinner("Searching documents..."):

            answer = ask_question(
                question,
                st.session_state.vector_db
            )

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer
        })

        st.rerun()
        
st.markdown("---")

st.markdown(
"""
<center>

Built with ❤️ using

Streamlit • LangChain • ChromaDB • Groq

</center>
""",
unsafe_allow_html=True
)