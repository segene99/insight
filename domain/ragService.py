from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

# Load the pre-trained RAG tokenizer
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

# Load the retriever component of the RAG model
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)

# Load the RAG model for token generation
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

# Prepare the input question
input_dict = tokenizer.prepare_seq2seq_batch("who holds the record in 100m freestyle", return_tensors="pt")

# Generate an answer
generated = model.generate(input_ids=input_dict["input_ids"])

# Print the answer (decoded from token IDs)
print(tokenizer.batch_decode(generated, skip_special_tokens=True)[0])

# should give michael phelps => sounds reasonable
