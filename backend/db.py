import streamlit as st
from pymongo import MongoClient


client = MongoClient(st.secrets["MONGO_URI"])

db = client["secureshare"]

users_collection = db["users"]
files_collection = db["files"]
logs_collection = db["logs"]
