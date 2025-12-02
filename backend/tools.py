import requests
from typing import List

references = []
users = [
        {"first_name": "Daisy", "Last_name": "Mendonca", "email": "daisy.mendonca@example.com"}
    ]

#------------
# User Management Tools
#------------

def get_users() -> list[dict]:
    return users

def add_user(first_name:str, last_name:str, email:str) -> dict:
    new_user = {"first_name": first_name, "last_name": last_name, "email": email}
    users.append(new_user)
    

#------------
# Paper Search Tool
#------------

def search_papers(query:str, limit:int=5) -> list[dict]:
    """
    Search academic papers using Semantic Scholar's public API.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": query, "limit": limit, "fields": "title,authors,year,abstract,url"}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("data", [])

#------------
# Get detailed paper info
#------------

def get_paper_details(paper_id:str) -> dict:
    """
    Get detailed information about a paper using its Semantic Scholar ID.
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "title,authors,year,abstract,url,citationCount,referenceCount"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

#------------
# Add reference tool
#------------

def add_reference(title: str, authors: list, year: int, url: str) -> dict:
    paper = {"title": title, "authors": authors, "year": year, "url": url}
    references.append(paper)
    return paper

#------------
# Get references tool
#------------
def get_references() -> list[dict]:
    return references