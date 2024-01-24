import os
import requests
from time import time
import multiprocessing
from dotenv import load_dotenv
load_dotenv()

# from utils._openai import generate_answer, rewrite
# from generate import rewrite, generate_answer
from rank_bm25 import BM25Okapi
# from trafilatura import fetch_url, extract
from newspaper import Article
from text_generation import generate_queries, response_gemini, classification_question, response_without_context


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')




def google_search(query, start, num):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx=84c7128382fe8459c&q={query}&safe=active&start={start}&num={num}"
    response = requests.get(url)
    return response.json()

def rrr_snippets(query):
    """
    use google search to retrieve snippets
    """
    questions = generate_queries(question=query)
    questions = [q.strip() for q in questions.split(";")]
    print(questions)

    snippets = []
    for question in questions:
        for i in range(1):
            response = google_search(query=question, start=i*10+1, num=10)
            if 'items' not in response.keys():
                response = google_search(query=response['spelling']['correctedQuery'], start=i*10+1, num=10)
            for item in response['items']:
                snippet = item['snippet']
                snippets.append(snippet)
    snippets = "\n".join(snippets)
    print(snippets)
    return response_gemini(question=query, context=snippets)

def get_paragraphs(url):
    try:
        # article = fetch_url(url)
        article = Article(url)
        article.download()
        article.parse()
        paragraphs = article.text.split("\n\n")
        new_paragraphs = []
        previous = ""
        for para in paragraphs:
            previous += " " + para
            if len(previous.split(" ")) > 50:
                new_paragraphs.append(f"SOURCE: {url}\n"+previous)
                previous = ""

        return new_paragraphs
        # if article is not None:
            # return extract(article).split("\n")
    except:
        return []
    
def rrr_pages(query, history="", n=20):
    """
    use google search to retrieve pages
    then get paragraphs from those pages
    finally, calculate bm25 scores for each paragraph
    """
    conversations = ""
    if history != "":
        # query = history + " " + query
        for item in history:
            conversations += f"{item['role']}: {item['content']}\n"
    print(conversations)
    classify_status = classification_question(query)
    print(classify_status)
    if "NO" in classify_status:
        return response_without_context(question=query, history=conversations)
    questions = generate_queries(question=query)
    questions = [q.strip() for q in questions.split(";")]
    print(questions)
    urls = []
    for question in questions:
        response = google_search(query=question, start=1, num=5)
        # print(response)
        if 'items' not in response.keys():
            response = google_search(query=response['spelling']['correctedQuery'], start=1, num=5)
        urls.extend([item['link'] for item in response['items']])
    print(urls)
    with multiprocessing.Pool(4) as pool:
        paras = pool.map(get_paragraphs, urls)
    
    paras = [para for para_list in paras for para in para_list]
    tokenized_corpus = [doc.split(" ") for doc in paras]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split(" ")
    bm25_results = bm25.get_top_n(tokenized_query, paras, n=n)
    docs = "\n\n".join(bm25_results)

    print(docs)
    return response_gemini(question=query, context=docs, history=conversations)

if __name__=="__main__":

    # print(get_paragraphs("https://thuvienphapluat.vn/hoi-dap-phap-luat/5CB41-hd-dieu-khien-xe-vuot-den-do-gay-tai-nan-giao-thong-co-bi-truy-cuu-hinh-su-hay-khong.html"))
    # Test pages
    start = time()
    
    query = "Lái xe máy vượt đèn đỏ thì phạt thế nào?"

    answer = rrr_pages(query=query, n=10)
    # answer = rrr_snippets(query=query)
    print("ANSWER:", answer)

    end = time()
    print("Time: ", end - start)