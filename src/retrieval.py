import requests
from bs4 import BeautifulSoup

class ArxivRetrievalAgent:
    BASE_URL = "http://export.arxiv.org/api/query"

    def get_papers(self, query: str, max_papers: int = 10):
        params = {"search_query": f"all:{query}", "start": 0, "max_results": max_papers}
        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")

        papers = []
        for entry in soup.find_all("entry"):
            papers.append({
                "title": entry.title.text.strip(),
                "abstract": entry.summary.text.strip(),
                "link": entry.id.text.strip(),
                "source": "arxiv"
            })
        return papers


class PubmedRetrievalAgent:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def get_papers(self, query: str, max_papers: int = 10):
        search_url = f"{self.BASE_URL}esearch.fcgi"
        fetch_url = f"{self.BASE_URL}efetch.fcgi"

        search_params = {"db": "pubmed", "term": query, "retmax": max_papers, "retmode": "json"}
        search_resp = requests.get(search_url, params=search_params, timeout=10)
        search_resp.raise_for_status()
        ids = search_resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        fetch_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}
        fetch_resp = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_resp.raise_for_status()

        soup = BeautifulSoup(fetch_resp.text, "xml")
        papers = []
        for article in soup.find_all("PubmedArticle"):
            title = article.ArticleTitle.text.strip() if article.ArticleTitle else "Untitled"
            abstract_tag = article.find("AbstractText")
            abstract = abstract_tag.text.strip() if abstract_tag else "No abstract"
            link = f"https://pubmed.ncbi.nlm.nih.gov/{article.PMID.text.strip()}"
            papers.append({"title": title, "abstract": abstract, "link": link, "source": "pubmed"})
        return papers
