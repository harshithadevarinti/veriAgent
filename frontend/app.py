import streamlit as st
import requests

st.title("VeriAgent — Hallucination Checker")

text = st.text_area("Paste an LLM response to fact-check:")

if st.button("Check"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Checking claims..."):
            try:
                response = requests.post("http://localhost:8000/check", json={"text": text})
            except requests.exceptions.ConnectionError:
                st.error("Could not reach the backend. Is it running on port 8000?")
                st.stop()

        if response.status_code != 200:
            st.error(f"Backend error {response.status_code}:")
            st.code(response.text)
        else:
            report = response.json()
            st.metric("Overall score", report["overall_score"])
            st.write(report["summary"])
            for claim in report["claims"]:
                color = {"SUPPORTED": "green", "REFUTED": "red", "NOT_ENOUGH_INFO": "orange"}[claim["label"]]
                st.markdown(f"**:{color}[{claim['label']}]** — {claim['claim']}")
                st.caption(f"{claim['rationale']} (resolved in {claim.get('iterations', 1)} iteration(s))")
                for ev in claim["evidence"]:
                    st.text(f"  ↳ ({ev['source']}, {ev['score']:.2f}) {ev['text']}")