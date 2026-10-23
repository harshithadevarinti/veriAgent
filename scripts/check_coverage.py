from retriever.retriever import retrieve

test_claims = [
    "Barack Obama was president of the United States.",
    "World War II ended in 1945.",
    "The Eiffel Tower is located in Paris.",
    "Albert Einstein developed the theory of relativity.",
    "The Great Wall of China is in China.",
]

for claim in test_claims:
    results = retrieve(claim, k=3)
    top_score = results[0].score if results else 0
    top_source = results[0].source if results else "none"
    print(f"{claim[:50]:50} | top_score={top_score:.2f} | top_source={top_source}")