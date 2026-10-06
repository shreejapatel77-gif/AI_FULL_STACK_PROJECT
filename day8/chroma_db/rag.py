from sentence_transformers import SentenceTransformer
import chromadb
import ollama
import streamlit as st


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()
st.title(":rainbow[*My Chatbot!!!*]")
# st.title("Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:
    st.header("Chat settings")
    personalities = {
        "Kid😎": "Give the answers like you are explaining to a 5 year old kid.Give the answer in 2 lines only",
        "Professor👨‍🏫": "You are an IIT professor.Explain the topics using correct terminology.Give the answer in 2-3 lines only",
        "Friendly👥": "You are a friend.Explain about friendship.Give the answer in 2-3 lines only"
    }
    personality = st.selectbox("Select a personality", personalities.keys())
    top_k = st.slider("Select no of top results",
                      min_value=1, max_value=5, value=3)
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
        with st.expander("Preview"):
            st.text(text)
        chunks = []
        chunk_size = 100
        chunk_overlap = 20
        step = chunk_size - chunk_overlap
        for i in range(0, len(text), step):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
        embeddings = model.encode(chunks)
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="My_Documents")
        ids = []
        for i in range(len(chunks)):
            ids.append(f"{uploaded_file.name}_{i}")
        collection.add(
            documents=chunks,
            ids=ids,
            embeddings=embeddings.tolist()
        )
    st.subheader("chat options")
    with st.container():
        if st.button("Clear Chat"):
            st.session_state.message = []
            st.success("Chat history deleted..")
    with st.expander("Chat History"):
        for msg in st.session_state.message:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
question = st.chat_input("Ask a question:")
if question:
    if uploaded_file:
        st.write(question)
        q_embedding = model.encode(question)
        results = collection.query(
            query_embeddings=[q_embedding.tolist()],
            n_results=top_k
        )
        retrieved_chunks = (results['documents'][0])
        retrieved_ids = results["ids"][0]
        context = '\n'.join(retrieved_chunks)
        prompt = f'''
        Answer the question using the context given below only.
        Question: {question}
        Context: {context}
        Answer:
        '''
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[{"role": "user",
                       "content": prompt}]
        )
        st.write(response["message"]["content"])
    else:
        with st.chat_message("user"):
            st.write(question)
        st.session_state.message.append(
            {"role": "user",
             "content": question}
        )
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="llama3.2:3b",
                messages=[{
                    "role": "system", "content": personalities[personality]
                }] + st.session_state.messages)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["message"]["content"]
        })
        with st.chat_message("assistant"):
            st.write("AI:", response["message"]["content"])
