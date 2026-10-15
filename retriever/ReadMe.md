# Retriever

`from retriever.retriever import retrieve`
`retrieve(query: str, k: int = 2) -> list[Evidence]` (score 0-1, higher = more relevant)

## Setup
1. pip install -r requirements.txt
2. Download chroma_db.zip: (https://drive.google.com/file/d/1Y59cvm-UG0q8OtPZpBZZtRkxrZYsvZe_/view?usp=sharing). Unzip to `retriever/chroma_db`.
3. Test: `python -m retriever.retriever`

## Corpus
FEVER Wikipedia dump subset: gold pages for 2,000 FEVER dev claims plus 5,000 random distractor pages (~7,200 chunks). Embeddings: all-MiniLM-L6-v2. Store: Chroma.

## Eval
- `eval/eval_claims.json`: 2,000 dev claims with gold pages (all indexed)
- `python -m retriever.eval_recall` for recall@k
- Results: recall@1 = 0.875, recall@5 = 0.956, recall@10 = 0.966
- Measured on a reduced index. Recall on the full Wikipedia dump will be lower. A hit means any gold evidence page appears in the top k.