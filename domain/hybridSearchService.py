from domain.keywordSearchService import search_keyword
from domain.ragService3 import search_documents
from sentence_transformers.cross_encoder import CrossEncoder


def combined_search(question, siteURLs):
    # Step 1: Retrieve Answers

    rag_answer = search_documents(question, siteURLs)
    print("]]]]]rag_answer]]]]]", rag_answer)
    page_contents = [doc.page_content for doc in rag_answer]
    bm25_answer = search_keyword(question, siteURLs)
    print("]]]]]bm25_answer]]]]]", bm25_answer)
    
    # Step 2: Use RRF to Combine Results
    combined_ranking = rrf([page_contents, bm25_answer])
    print("&&&&combined_ranking&&&&&", combined_ranking[0])

    # Step 3: Re-ranking using Cross-Encoder
    # model = CrossEncoder('cross-encoder/stsb-distilroberta-base')  # replace 'model_name_or_path' with your model name or path
    # sentences = [[question, string] for doc in combined_ranking for string in doc]
    # scores = model.predict(sentences)

    # scores = model.predict([[question, doc] for doc in combined_ranking])
    # Pairing scores with documents and sorting by scores
    # ranked_results = sorted(zip(scores, combined_ranking), key=lambda x: x[0], reverse=True)
    # print("]]]]]ranked_results]]]]]", ranked_results)
    # Return the top-ranked document after re-ranking
    # return ranked_results[0][1]
    return combined_ranking[0]


    # Return the top answer after combining
    # return combined_ranking[0]

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

