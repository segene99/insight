from domain.keywordSearchService import search_keyword
from domain.ragService3 import search_documents


def combined_search(question, siteURLs):
    # Step 1: Retrieve Answers
    print("]]]]]1]]]]]")
    rag_answer = search_documents(question, siteURLs)
    print("]]]]]2]]]]]", rag_answer)
    page_contents = [doc.page_content for doc in rag_answer]
    bm25_answer = search_keyword(question, siteURLs)
    print("]]]]]3]]]]]", bm25_answer)
    # Step 2: Create Ranked Lists (assuming the answers are the top results)
    # rag_ranked = [page_contents]
    # bm25_ranked = [bm25_answer]
    
    # Step 3: Apply RRF
    # combined_ranking = rrf([rag_ranked, bm25_ranked])
    combined_ranking = rrf([page_contents, bm25_answer])

    # Return the top answer after combining
    return combined_ranking[0]

def rrf(rankings, k=60):
    # Given you're dealing with single answers, 
    # the rankings are straightforward. 
    # For a more complex setting, adapt this function accordingly.
    
    rrf_scores = {}

    for rank, item in enumerate(rankings):
            rrf_score = 1.0 / (k + rank)
            # Convert the item to a tuple if it's a list
            key = tuple(item) if isinstance(item, list) else item
            if key in rrf_scores:
                rrf_scores[key] += rrf_score
            else:
                rrf_scores[key] = rrf_score


    # Sorting items based on RRF scores in descending order
    sorted_items = sorted(rrf_scores, key=rrf_scores.get, reverse=True)

    return sorted_items

