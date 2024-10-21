import streamlit as st
import requests

def getRepo(repo_name):
    url = f'https://api.github.com/repos/{repo_name}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        st.write(f"Repository: {data['full_name']}")
        st.write(f"Description: {data['description']}")
        st.write(f"Stars: {data['stargazers_count']}")
        st.write(f"Forks: {data['forks_count']}")
        st.write(f"Last updated: {data['updated_at']}")
    else:
        st.error("Error retrieving data from GitHub: " + response.text)