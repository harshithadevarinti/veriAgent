import json
import time
from agents.pipeline import verify_response
from retriever.retriever import retrieve
from eval.metrics import label_metrics

with open("eval/test_set.json", encoding="utf-8") as f:
    test_cases = json.load(f)

LABEL_MAP = {"SUPPORTS": "SUPPORTED", "REFUTES": "REFUTED"}

y_true, y_pred = [], []

for case in test_cases:
    expected = LABEL_MAP.get(case["label"], case["label"])
    verdicts = verify_response(case["claim"], retrieve)
    predicted = verdicts[0].label if verdicts else "NOT_ENOUGH_INFO"
    y_true.append(expected)
    y_pred.append(predicted)
    print(f"{case['claim'][:50]:50} | expected={expected:15} | got={predicted}")
    time.sleep(15)

print("\nMetrics:", label_metrics(y_true, y_pred))