import streamlit as st
import pandas as pd
import plotly.express as px
import json
from src.data_loader import load_csv, build_schema, get_sample, get_summary
from src.analyser import ask_question

st.set_page_config(page_title="InSight", page_icon="◈", layout="wide")

st.title("◈ InSight")
st.caption("Ask questions about your data in plain English.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "df" not in st.session_state:
    st.session_state.df = None
if "schema" not in st.session_state:
    st.session_state.schema = None

with st.sidebar:
    st.header("Dataset")
    option = st.radio("Choose data source", ["Upload CSV", "Demo: Companies House"])

    if option == "Upload CSV":
        file = st.file_uploader("Upload a CSV file", type=["csv"])
        if file and st.session_state.get("uploaded_filename") != file.name:
            st.session_state.df = load_csv(file)
            st.session_state.schema = build_schema(st.session_state.df)
            st.session_state.history = []
            st.session_state.messages = []
            st.session_state.uploaded_filename = file.name

    elif option == "Demo: Companies House":
        st.session_state.df = load_csv("demo_data/companies_house.csv")
        st.session_state.schema = build_schema(st.session_state.df)

    if st.session_state.df is not None:
        summary = get_summary(st.session_state.df)
        st.success(f"{summary['rows']} rows · {summary['columns']} columns")
        if summary['rows'] > 300:
            st.warning("Large dataset detected — analysis will use a sample of 300 rows for speed.")
        st.write("**Columns:**")
        for col in summary["column_names"]:
            st.caption(f"· {col}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "stats" in msg and msg["stats"]:
            cols = st.columns(len(msg["stats"]))
            for i, stat in enumerate(msg["stats"]):
                with cols[i]:
                    st.metric(label=stat["label"], value=stat["value"], help=stat.get("sub"))
        if "chart" in msg and msg["chart"].get("type"):
            chart = msg["chart"]
            chart_df = pd.DataFrame({"label": chart["labels"], "value": chart["values"]})
            if chart["type"] == "bar":
                fig = px.bar(chart_df, x="label", y="value", title=chart.get("title"))
            elif chart["type"] == "line":
                fig = px.line(chart_df, x="label", y="value", title=chart.get("title"))
            elif chart["type"] == "doughnut":
                fig = px.pie(chart_df, names="label", values="value", title=chart.get("title"), hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        if "followups" in msg and msg["followups"]:
            st.caption("You might also ask:")
            for q in msg["followups"]:
                if st.button(q, key=f"{q}_{id(msg)}"):
                    st.session_state.pending_question = q

question = st.chat_input("Ask a question about your data...")

if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

if question:
    if st.session_state.df is None:
        st.warning("Please load a dataset first using the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("Analysing..."):
            try:
                sample = get_sample(st.session_state.df)
                max_rows = min(300, len(st.session_state.df))
                data_json = st.session_state.df.head(max_rows).to_json(orient="records")
                result, st.session_state.history = ask_question(
                    st.session_state.schema,
                    sample,
                    data_json,
                    question,
                    st.session_state.history
                )
                msg = {
                    "role": "assistant",
                    "content": result["insight"],
                    "stats": result.get("stats", []),
                    "chart": result.get("chart", {}),
                    "followups": result.get("followups", [])
                }
                st.session_state.messages.append(msg)
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {e}",
                    "stats": [],
                    "chart": {},
                    "followups": []
                })
        st.rerun()