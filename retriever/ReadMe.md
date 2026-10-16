# Retriever

`from retriever.retriever import retrieve`
`retrieve(query: str, k: int = 2) -> list[Evidence]` (score 0-1, higher = more relevant)

## Setup
1. pip install -r requirements.txt
2. Download chroma_db.zip: (https://drive.google.com/file/d/1Y59cvm-UG0q8OtPZpBZZtRkxrZYsvZe_/view?usp=sharing). Unzip to `retriever/chroma_db`.
3. Test: `python -m retriever.retriever`

## Corpus
FEVER Wikipedia dump subset: gold pages for 2,000 FEVER dev claims plus 5,000 random distractor pages (~7,200 chunks). Embeddings: all-MiniLM-L6-v2. Store: Chroma.

## Reranker
`retrieve(query, k=5, rerank=True)` retrieves 30 dense candidates and reranks them with a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`). Default is `rerank=False`. It adds latency per query. The first call downloads the model (~90 MB).

## Eval
- `eval/eval_claims.json`: 2,000 FEVER dev claims with gold pages (all indexed)
- Without reranker: `python -m retriever.eval_recall`
- With reranker: `python -m retriever.eval_recall rerank`

| | recall@1 | recall@5 | recall@10 |
|---|---|---|---|
| Dense only | 0.875 | 0.956 | 0.966 |
| Dense + reranker | 0.958 | 0.977 | 0.977 |

1,990 claims evaluated. A hit means any gold evidence page appears in the top k.
Measured on a reduced index (gold pages for 2,000 dev claims + 5,000 random distractors). Recall on the full Wikipedia dump will be lower.