import streamlit as st
import requests

st.title("VeriAgent — Hallucination Checker")

text = st.text_area("Paste an LLM response to fact-check:")

if st.button("Check") and text:
    response = requests.post("http://localhost:8000/check", json={"text": text})
    report = response.json()

    st.metric("Overall score", report["overall_score"])
    st.write(report["summary"])

    for claim in report["claims"]:
        color = {"SUPPORTED": "green", "REFUTED": "red", "NOT_ENOUGH_INFO": "orange"}[claim["label"]]
        st.markdown(f"**:{color}[{claim['label']}]** — {claim['claim']}")
        st.caption(claim["rationale"])
        for ev in claim["evidence"]:
            st.text(f"  ↳ ({ev['source']}, {ev['score']:.2f}) {ev['text']}")