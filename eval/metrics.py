from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def label_metrics(y_true: list[str], y_pred: list[str]) -> dict:
    """Accuracy + macro F1 for 3-way label classification (FEVER-style)."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
    }


def hallucination_metrics(y_true: list[bool], y_pred: list[bool]) -> dict:
    """Binary detection metrics (HaluEval / RAGTruth)."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }


def retrieval_metrics(relevant_ids: list[set], retrieved_ids: list[list]) -> dict:
    """Recall@k averaged across queries. relevant_ids[i] is the gold set
    for query i; retrieved_ids[i] is the ranked list of ids returned."""
    recalls = []
    for gold, retrieved in zip(relevant_ids, retrieved_ids):
        if not gold:
            continue
        hit = len(gold & set(retrieved)) / len(gold)
        recalls.append(hit)
    return {"recall_at_k": sum(recalls) / len(recalls) if recalls else 0.0}