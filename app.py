import os

import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="Student Marks", page_icon="📚")
st.title("Cincy Solutions - Student Marks")


@st.cache_resource
def get_collection():
    client = MongoClient(
        os.getenv("MONGO_URI", "mongodb://mongodb:27017"),
        serverSelectionTimeoutMS=3000,
    )
    return client["school"]["marks"]


collection = get_collection()
with st.form("marks_form"):
    name = st.text_input("Student Name")
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Save Marks")

if submitted:
    if not name.strip() or not subject.strip():
        st.error("Student name and subject are required.")
    else:
        try:
            collection.insert_one(
                {"name": name.strip(), "subject": subject.strip(), "marks": int(marks)}
            )
            st.success("Marks saved successfully.")
        except PyMongoError as exc:
            st.error(f"Database error: {exc}")

st.subheader("Saved Marks")
try:
    rows = list(collection.find({}, {"_id": 0}).sort("name", 1))
    if rows:
        st.dataframe(rows, width="stretch")
    else:
        st.info("No marks saved yet.")
except PyMongoError as exc:
    st.error(f"Database error: {exc}")
