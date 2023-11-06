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
    combined_ranking = rrf([page_contents, bm25_answer])
    print("&&&&combined_ranking&&&&&", combined_ranking[0])

    return combined_ranking

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

