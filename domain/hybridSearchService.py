from collections import defaultdict
from domain.keywordSearchService import search_keyword
from domain.ragService3 import search_documents
from sentence_transformers.cross_encoder import CrossEncoder
import asyncio

async def combined_search(question, siteURLs):
    print("[siteUrls]",siteURLs)
    rag_answer, bm25_answer = await asyncio.gather(
        search_documents(question, siteURLs),
        search_keyword(question, siteURLs)
    )
    # Step 1: Retrieve Answers
    print("]]]]]rag_answer]]]]]", rag_answer)
    page_contents = [doc.page_content for doc in rag_answer]
    print("]]]]]bm25_answer]]]]]", bm25_answer)
    
    # Step 2: Use RRF to Combine Results
    combined_ranking = rrf(page_contents, bm25_answer)

    return combined_ranking

def rrf(rag_rankings, bm25_rankings, k=60):
    # Create a dictionary to store RRF scores
    rrf_scores = defaultdict(float)
    
    # Process RAG rankings
    for rank, document in enumerate(rag_rankings, start=1):
        rrf_scores[document] += 1 / (k + rank)

    # Process BM25 rankings
    for rank, document in enumerate(bm25_rankings, start=1):
        rrf_scores[document] += 1 / (k + rank)

    # Sorting items based on RRF scores in descending order
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return sorted documents based on RRF score
    return [doc for doc, _ in sorted_items]
'''
def rrf(rankings, k=60):
    print("=====RRF======")
    rrf_scores = {}
    for rank, item in enumerate(rankings):
            rrf_score = 1.0 / (k + rank)
            # 튜플 -> 리스트 변환
            key = tuple(item) if isinstance(item, list) else item
            if key in rrf_scores:
                rrf_scores[key] += rrf_score
            else:
                rrf_scores[key] = rrf_score

    # Sorting items based on RRF scores in descending order
    sorted_items = sorted(rrf_scores, key=rrf_scores.get, reverse=True)
    return sorted_items
'''
