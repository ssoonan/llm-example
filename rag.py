from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

import os

from third_parties.naver_search import fetch_naver_data

openai_client = OpenAI(api_key=os.environ['OPENAI_KEY'])


pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index(name="stock-recommendations")


def embed_text_with_keywords(text, company):
    context = f"{company}\n{text}"
    response = openai_client.embeddings.create(input=context, model="text-embedding-3-small")
    return response.data[0].embedding


def store_news_in_pinecone(news_articles, stock):
    for article in news_articles:
        vector = embed_text_with_keywords(article["description"], stock)
        metadata = {
            "title": article["title"],
            "link": article["link"],
            "date": article["pubDate"],
            "chunk": article["description"]
        }
        index.upsert([(article["link"], vector, metadata)])


def query_pinecone(query, top_k=50):
    results = index.query(vector=query, top_k=top_k, include_metadata=True)
    return results["matches"]


def generate_contextual_recommendation(company, relevant_news, keywords):
    news_summaries = "\n".join([f"""
    제목: {news['metadata']['title']}\n
    요약: {news['metadata']['chunk']}\n
    링크: {news['metadata']['link']}""" for news in relevant_news])
    prompt = f"""
    사용자가 관심있는 회사는 다음과 같습니다: {company}.\n
    사용자가 관심을 가지는 회사의 최신 기사들입니다.{news_summaries}\n
    이 회사와 관련된 키워드들은 이러합니다.{keywords}\n
    해당 기사들 단기적인 변화가 아니라 이 종목에 영향을 줄 수 있는 경제적 흐름이 포함된 5개의 경제 기사와 링크를 추출해줘:\n"""
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 사용자의 주식 포트폴리오 관리에 도움을 주는 펀드 매니저입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content


# 예시 회사 2곳
stock_keywords = {
    "고려신용정보": ["신용평가", "채권추심", "재무 실적", "경제 전망", "정부 규제"], 
    "KISCO홀딩스": ["철강 산업", "원자재 가격", "무역 정책", "인플레이션", "환경 규제"]}
# 회사당 키워드 5개, 각 키워드당 50개 뉴스 검색

for stock in stock_keywords:
    for keyword in stock_keywords[stock]:
        naver_data = fetch_naver_data(keyword)
        store_news_in_pinecone(naver_data, stock)


# Example usage:
for stock in stock_keywords:
    stock_query = f"{stock} 관련된 경제 기사를 찾아줘"
    refined_query_embedding = embed_text_with_keywords(stock_query, stock)
    relevant_news_results = query_pinecone(refined_query_embedding)
    recommendation = generate_contextual_recommendation(stock, relevant_news_results, stock_keywords[stock])
    print(recommendation)
