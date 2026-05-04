import streamlit as st
import pandas as pd

from src.data_loader import load_file, load_csv, build_schema, build_multi_schema, get_sample, get_summary
from src.analyser import ask_question
from src.charts import render_chart, render_correlation_heatmap
from src.profiler import generate_profile, get_quality_warnings, generate_starter_questions, detect_time_columns
from src.workspace import list_workspaces, save_workspace, load_workspace, delete_workspace
from src.reporter import generate_html_report
from src.connectors import load_from_sql, load_from_google_sheets

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="InSight", layout="wide")

# Font must be injected as a <link> tag — @import inside st.markdown style blocks is unreliable
st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown("""
<style>

/* ── Font ──────────────────────────────────────────────────────────── */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* CRITICAL: Restore Material Symbols icon font.
   Streamlit renders all Material icons as spans with data-testid="stIconMaterial".
   The wildcard font rule above breaks them without this specific override. */
[data-testid="stIconMaterial"],
.material-symbols-rounded,
[class*="material-symbols"] {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    -webkit-font-feature-settings: 'liga' !important;
    font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ── App background ─────────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}
[data-testid="stMain"] {
    background-color: #FFFFFF !important;
}
.main .block-container, [data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #F7F7F5 !important;
    border-right: 1px solid #E8E7E3 !important;
}
[data-testid="stSidebar"] > div > div > div {
    background-color: #F7F7F5 !important;
}

/* ── Typography ───────────────────────────────────────────────────── */
h1, h2, h3, h4 {
    letter-spacing: -0.03em !important;
    color: #18181B !important;
}
h1 { font-size: 2.5rem !important; font-weight: 700 !important; }
h2 { font-size: 1.5rem !important; font-weight: 600 !important; }
h3, h4 { font-size: 1rem !important; font-weight: 600 !important; }
p { color: #52525B !important; line-height: 1.7 !important; }
label { color: #52525B !important; font-size: 0.875rem !important; }

/* ── Tabs ─────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #E8E7E3 !important;
    background: transparent !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #71717A !important;
    padding: 0.75rem 1.25rem !important;
    background: transparent !important;
    transition: color 0.15s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    border-bottom: 2px solid #2563EB !important;
    color: #18181B !important;
    font-weight: 600 !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
    color: #3F3F46 !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton > button,
.stDownloadButton > button {
    background: #FFFFFF !important;
    border: 1px solid #E2E1DD !important;
    border-radius: 8px !important;
    color: #18181B !important;
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    padding: 0.375rem 0.875rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    transition: background 0.15s, border-color 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #F4F4F5 !important;
    border-color: #D1D0CC !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
.stButton > button:active,
.stDownloadButton > button:active {
    background: #EBEBEB !important;
    box-shadow: none !important;
}

/* ── Metric cards ─────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #FAFAF9 !important;
    border: 1px solid #E8E7E3 !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.625rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #18181B !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.6875rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: #A1A1AA !important;
}

/* ── Bordered containers (Profile cards) ─────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FAFAF9 !important;
    border-color: #E8E7E3 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}

/* ── Chat messages ────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: #FAFAF9 !important;
    border: 1px solid #E8E7E3 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    margin-bottom: 0.75rem !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #EFF6FF !important;
    border-color: #BFDBFE !important;
}

/* ── Chat input ───────────────────────────────────────────────────── */
[data-testid="stChatInputContainer"] {
    border-radius: 12px !important;
    border: 1.5px solid #E2E1DD !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
    background: #FFFFFF !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08), 0 4px 12px rgba(0,0,0,0.06) !important;
}

/* ── Text / select inputs ─────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E1DD !important;
    border-radius: 8px !important;
    color: #18181B !important;
    font-size: 0.875rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}

/* ── Expanders ────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E7E3 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Dividers ─────────────────────────────────────────────────────── */
hr { border-color: #E8E7E3 !important; }

/* ── Captions / small text ────────────────────────────────────────── */
small, .stCaption, [data-testid="stCaptionContainer"] {
    font-size: 0.8125rem !important;
    color: #A1A1AA !important;
    line-height: 1.5 !important;
}

/* ── File uploader ────────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
    border-radius: 10px !important;
    border: 1.5px dashed #D4D2CE !important;
    background: #FAFAF9 !important;
    transition: border-color 0.15s, background 0.15s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #2563EB !important;
    background: #EFF6FF !important;
}

/* ── Dataframe ────────────────────────────────────────────────────── */
[data-testid="stDataFrameResizable"] {
    border: 1px solid #E8E7E3 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Selectbox ────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E1DD !important;
    border-radius: 8px !important;
}

/* ── Alerts ───────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.875rem !important;
}

/* ── Radio labels ─────────────────────────────────────────────────── */
[data-testid="stRadio"] label {
    font-size: 0.875rem !important;
    color: #3F3F46 !important;
}

</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "datasets": {},        # {display_name: DataFrame}
    "active_key": None,    # key into datasets
    "messages": [],
    "history": [],
    "profile": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helpers ───────────────────────────────────────────────────────────────────
def _active_df() -> pd.DataFrame | None:
    key = st.session_state.active_key
    return st.session_state.datasets.get(key) if key else None


def _register_dataset(name: str, df: pd.DataFrame, reset_chat: bool = True) -> None:
    st.session_state.datasets[name] = df
    st.session_state.active_key = name
    st.session_state.profile = generate_profile(df)
    if reset_chat:
        st.session_state.messages = []
        st.session_state.history = []


def _activate(key: str) -> None:
    st.session_state.active_key = key
    df = st.session_state.datasets[key]
    st.session_state.profile = generate_profile(df)


def _schema() -> str:
    if len(st.session_state.datasets) > 1:
        return build_multi_schema(st.session_state.datasets, st.session_state.active_key)
    df = _active_df()
    return build_schema(df) if df is not None else ""


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:0.25rem 0 0.75rem 0;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">'
        '<div style="width:28px;height:28px;background:linear-gradient(135deg,#2563EB 0%,#7C3AED 100%);'
        'border-radius:7px;flex-shrink:0;"></div>'
        '<span style="font-size:1.125rem;font-weight:700;letter-spacing:-0.03em;color:#18181B;">InSight</span>'
        '</div>'
        '<p style="font-size:0.75rem;color:#A1A1AA;margin:0;line-height:1.4;">AI-powered data analysis</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # -- Data source --
    st.markdown(
        '<p style="font-size:0.6875rem;font-weight:600;text-transform:uppercase;'
        'letter-spacing:0.07em;color:#A1A1AA;margin-bottom:0.5rem;">Data source</p>',
        unsafe_allow_html=True,
    )
    source = st.radio(
        "source",
        ["Upload file(s)", "Google Sheets", "SQL Database", "Demo: Companies House"],
        label_visibility="collapsed",
    )

    if source == "Upload file(s)":
        files = st.file_uploader(
            "CSV or Excel", type=["csv", "xlsx", "xls"],
            accept_multiple_files=True, label_visibility="collapsed",
        )
        if files:
            for f in files:
                if f.name not in st.session_state.datasets:
                    with st.spinner(f"Loading {f.name}…"):
                        _register_dataset(f.name, load_file(f), reset_chat=False)
            st.session_state.active_key = st.session_state.active_key or (files[0].name if files else None)

    elif source == "Google Sheets":
        gs_url = st.text_input("Paste the sheet URL", placeholder="https://docs.google.com/spreadsheets/d/…")
        if st.button("Load sheet", use_container_width=True) and gs_url:
            with st.spinner("Fetching sheet…"):
                try:
                    df = load_from_google_sheets(gs_url)
                    _register_dataset("Google Sheet", df)
                    st.success(f"Loaded {len(df):,} rows")
                except ValueError as e:
                    st.error(str(e))

    elif source == "SQL Database":
        conn_str = st.text_input("Connection string", placeholder="sqlite:///mydb.db")
        query = st.text_area("SQL query", placeholder="SELECT * FROM my_table LIMIT 10000", height=80)
        if st.button("Run query", use_container_width=True) and conn_str and query:
            with st.spinner("Querying database…"):
                try:
                    df = load_from_sql(conn_str, query)
                    _register_dataset(f"SQL: {query[:30]}…", df)
                    st.success(f"Loaded {len(df):,} rows")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    elif source == "Demo: Companies House":
        if "demo_loaded" not in st.session_state:
            with st.spinner("Loading demo…"):
                _register_dataset("Companies House (demo)", load_csv("demo_data/companies_house.csv"))
                st.session_state.demo_loaded = True

    # -- Loaded datasets --
    if st.session_state.datasets:
        st.divider()
        st.markdown(
            '<p style="font-size:0.6875rem;font-weight:600;text-transform:uppercase;'
            'letter-spacing:0.07em;color:#A1A1AA;margin-bottom:0.5rem;">Loaded datasets</p>',
            unsafe_allow_html=True,
        )
        for key in list(st.session_state.datasets.keys()):
            col_a, col_b = st.columns([4, 1])
            is_active = key == st.session_state.active_key
            label = f"**{key}**" if is_active else key
            with col_a:
                if st.button(label, key=f"activate_{key}", use_container_width=True):
                    _activate(key)
                    st.rerun()
            with col_b:
                if st.button("✕", key=f"remove_{key}"):
                    del st.session_state.datasets[key]
                    if st.session_state.active_key == key:
                        remaining = list(st.session_state.datasets.keys())
                        st.session_state.active_key = remaining[0] if remaining else None
                        if st.session_state.active_key:
                            _activate(st.session_state.active_key)
                    st.rerun()

        df = _active_df()
        if df is not None:
            s = get_summary(df)
            st.success(f"{s['rows']:,} rows · {s['columns']} cols")
            if s["rows"] > 300:
                st.info("Analysis runs on the full dataset via code execution.")

        # -- Join --
        if len(st.session_state.datasets) >= 2:
            with st.expander("Join datasets"):
                keys = list(st.session_state.datasets.keys())
                left_key = st.selectbox("Left table", keys, key="join_left")
                right_key = st.selectbox("Right table", [k for k in keys if k != left_key], key="join_right")
                left_df = st.session_state.datasets[left_key]
                right_df = st.session_state.datasets[right_key]
                j1, j2, j3 = st.columns(3)
                with j1:
                    left_col = st.selectbox("Left key", left_df.columns, key="jlc")
                with j2:
                    right_col = st.selectbox("Right key", right_df.columns, key="jrc")
                with j3:
                    how = st.selectbox("Type", ["inner", "left", "right", "outer"], key="jhow")
                if st.button("Join", use_container_width=True):
                    try:
                        joined = pd.merge(left_df, right_df, left_on=left_col, right_on=right_col, how=how)
                        joined_name = f"{left_key} × {right_key}"
                        _register_dataset(joined_name, joined, reset_chat=False)
                        st.success(f"{len(joined):,} rows after join")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

    # -- Workspaces --
    st.divider()
    st.markdown(
        '<p style="font-size:0.6875rem;font-weight:600;text-transform:uppercase;'
        'letter-spacing:0.07em;color:#A1A1AA;margin-bottom:0.5rem;">Workspaces</p>',
        unsafe_allow_html=True,
    )
    ws_name = st.text_input("Save as", placeholder="my-analysis", label_visibility="collapsed")
    if st.button("Save workspace", use_container_width=True) and ws_name and st.session_state.datasets:
        save_workspace(ws_name, st.session_state.datasets, st.session_state.messages)
        st.success("Saved.")

    workspaces = list_workspaces()
    if workspaces:
        ws_options = {w["name"]: w for w in workspaces}
        selected_ws = st.selectbox(
            "Load workspace", [""] + list(ws_options.keys()), label_visibility="collapsed"
        )
        if selected_ws:
            w1, w2 = st.columns(2)
            with w1:
                if st.button("Load", use_container_width=True):
                    dsets, msgs, meta = load_workspace(selected_ws)
                    st.session_state.datasets = dsets
                    st.session_state.active_key = list(dsets.keys())[0] if dsets else None
                    if st.session_state.active_key:
                        _activate(st.session_state.active_key)
                    st.session_state.messages = msgs
                    st.session_state.history = []
                    st.rerun()
            with w2:
                if st.button("Delete", use_container_width=True):
                    delete_workspace(selected_ws)
                    st.rerun()

    # -- Actions --
    if st.session_state.datasets:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("New chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.history = []
                st.rerun()
        with c2:
            if st.session_state.messages:
                html = generate_html_report(st.session_state.messages)
                st.download_button(
                    "Export HTML",
                    data=html,
                    file_name="insight_report.html",
                    mime="text/html",
                    use_container_width=True,
                )

        if st.session_state.messages:
            chat_text = "\n\n".join(
                f"{'You' if m['role'] == 'user' else 'InSight'}: {m['content']}"
                for m in st.session_state.messages
            )
            st.download_button(
                "Export TXT",
                data=chat_text,
                file_name="insight_conversation.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ── Main area ─────────────────────────────────────────────────────────────────
df = _active_df()

if df is None:
    st.markdown(
        '<div style="padding:2.5rem 0 2rem 0;">'
        '<div style="display:flex;align-items:center;gap:0.875rem;margin-bottom:1rem;">'
        '<div style="width:48px;height:48px;background:linear-gradient(135deg,#2563EB 0%,#7C3AED 100%);'
        'border-radius:12px;flex-shrink:0;box-shadow:0 4px 14px rgba(37,99,235,0.25);"></div>'
        '<h1 style="font-size:2.5rem;font-weight:700;letter-spacing:-0.04em;color:#18181B;margin:0;">InSight</h1>'
        '</div>'
        '<p style="font-size:1.125rem;color:#71717A;font-weight:400;margin:0;line-height:1.6;">'
        'Ask questions about your data in plain English.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown(
            '<div style="background:#FAFAF9;border:1px solid #E8E7E3;border-radius:12px;'
            'padding:1.25rem 1.5rem;height:100%;">'
            '<p style="font-size:0.8125rem;font-weight:600;color:#18181B;margin:0 0 0.375rem 0;'
            'letter-spacing:-0.01em;">Load data</p>'
            '<p style="font-size:0.8125rem;color:#71717A;margin:0;line-height:1.6;">'
            'Upload CSV or Excel files, connect to a SQL database, or pull from Google Sheets using the sidebar.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    with cb:
        st.markdown(
            '<div style="background:#FAFAF9;border:1px solid #E8E7E3;border-radius:12px;'
            'padding:1.25rem 1.5rem;height:100%;">'
            '<p style="font-size:0.8125rem;font-weight:600;color:#18181B;margin:0 0 0.375rem 0;'
            'letter-spacing:-0.01em;">Ask anything</p>'
            '<p style="font-size:0.8125rem;color:#71717A;margin:0;line-height:1.6;">'
            'InSight runs real Python code on your full dataset to give exact answers, metrics, and charts.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    with cc:
        st.markdown(
            '<div style="background:#FAFAF9;border:1px solid #E8E7E3;border-radius:12px;'
            'padding:1.25rem 1.5rem;height:100%;">'
            '<p style="font-size:0.8125rem;font-weight:600;color:#18181B;margin:0 0 0.375rem 0;'
            'letter-spacing:-0.01em;">Explore</p>'
            '<p style="font-size:0.8125rem;color:#71717A;margin:0;line-height:1.6;">'
            'Browse your data, see auto-generated column statistics in Profile, or save your work as a Workspace.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

else:
    for level, msg in get_quality_warnings(df):
        if level == "error":
            st.error(msg)
        else:
            st.warning(msg)

    chat_tab, data_tab, profile_tab, help_tab = st.tabs(["💬 Chat", "📋 Data", "📊 Profile", "ℹ️ Help"])

    # ── Chat tab ──────────────────────────────────────────────────────────────
    with chat_tab:
        for msg_idx, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("stats"):
                    scols = st.columns(len(msg["stats"]))
                    for i, stat in enumerate(msg["stats"]):
                        with scols[i]:
                            st.metric(label=stat["label"], value=stat["value"], help=stat.get("sub"))
                if msg.get("chart"):
                    render_chart(msg["chart"])
                if msg.get("followups"):
                    st.caption("You might also ask:")
                    bcols = st.columns(len(msg["followups"]))
                    for q_idx, q in enumerate(msg["followups"]):
                        with bcols[q_idx]:
                            if st.button(q, key=f"followup_{msg_idx}_{q_idx}"):
                                st.session_state.pending_question = q

        if not st.session_state.messages:
            st.markdown("#### Where would you like to start?")
            time_cols = detect_time_columns(df)
            if time_cols:
                st.caption(f"Time column detected: **{time_cols[0]}** — you can ask about trends over time.")
            if len(st.session_state.datasets) > 1:
                st.caption(f"**{len(st.session_state.datasets)} datasets loaded** — you can ask questions that span all of them.")
            starters = generate_starter_questions(df)
            grid = st.columns(2)
            for i, q in enumerate(starters):
                with grid[i % 2]:
                    if st.button(q, key=f"starter_{i}", use_container_width=True):
                        st.session_state.pending_question = q

    # ── Data tab ──────────────────────────────────────────────────────────────
    with data_tab:
        if len(st.session_state.datasets) > 1:
            view_key = st.selectbox("Dataset", list(st.session_state.datasets.keys()), key="data_view_sel")
            view_df = st.session_state.datasets[view_key]
        else:
            view_df = df
        s = get_summary(view_df)
        st.caption(f"{s['rows']:,} rows · {s['columns']} columns")
        st.dataframe(view_df, use_container_width=True, height=520)

    # ── Profile tab ───────────────────────────────────────────────────────────
    with profile_tab:
        profile = st.session_state.profile or {}
        numeric_cols = [c for c, v in profile.items() if v["kind"] == "numeric"]
        cat_cols = [c for c, v in profile.items() if v["kind"] == "categorical"]

        if numeric_cols:
            st.markdown("**Numeric columns**")
            ncols = st.columns(3)
            for i, col in enumerate(numeric_cols):
                p = profile[col]
                with ncols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"**{col}**")
                        st.caption(f"Min: {p['min']}  ·  Max: {p['max']}")
                        st.caption(f"Mean: {p['mean']}  ·  Median: {p['median']}")
                        if p["null_pct"] > 0:
                            st.caption(f"⚠ {p['null_pct']}% null")

        if cat_cols:
            st.markdown("**Categorical columns**")
            ccols = st.columns(3)
            for i, col in enumerate(cat_cols):
                p = profile[col]
                with ccols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"**{col}**")
                        st.caption(f"{p['unique']} unique values")
                        for val, count in list(p.get("top", {}).items())[:3]:
                            st.caption(f"· {val}: {count:,}")
                        if p["null_pct"] > 0:
                            st.caption(f"⚠ {p['null_pct']}% null")

        if len(numeric_cols) >= 2:
            st.markdown("**Correlation matrix**")
            render_correlation_heatmap(df)

    # ── Help tab ──────────────────────────────────────────────────────────────
    with help_tab:
        st.markdown(
            '<h2 style="font-size:1.5rem;font-weight:700;letter-spacing:-0.03em;'
            'margin-bottom:0.5rem;">What can I do with InSight?</h2>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "InSight is a specialised data analysis tool — not a general chatbot. "
            "The key difference from using Claude directly: **InSight runs real Python code "
            "on your full dataset**, so every number in every answer is exact, regardless of "
            "how large your file is."
        )
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💬 Asking questions")
            st.markdown("""
Ask anything in plain English. InSight will compute the answer by running pandas code on your data:

- *"What is the average revenue by region?"*
- *"Which product had the most returns last quarter?"*
- *"Is there a correlation between price and sales volume?"*
- *"Show me the top 10 customers by total spend"*
- *"What percentage of orders were delivered late?"*

Every answer includes key metrics and a chart where relevant, plus three suggested follow-up questions.
""")

            st.markdown("#### 📊 Charts & metrics")
            st.markdown("""
InSight automatically picks the right chart type (bar, line, or doughnut) and surfaces 2–4 key metrics alongside each answer. Just ask — you don't need to specify the format.
""")

            st.markdown("#### 🔀 Multi-dataset analysis")
            st.markdown("""
Upload multiple files and InSight is aware of all of them. Use the **Join** panel to merge datasets on a shared key column, then ask questions that span both files — e.g. *"Join customers and orders, then show me revenue by customer segment."*
""")

        with col2:
            st.markdown("#### 📋 Data & Profile tabs")
            st.markdown("""
- **Data tab** — browse and sort your raw data with full filtering
- **Profile tab** — instant column statistics (min, max, mean, top values, null %) and a correlation heatmap for numeric columns, generated automatically on load
""")

            st.markdown("#### 💾 Workspaces")
            st.markdown("""
Save your datasets and conversation to a named workspace so you can close the app and pick up exactly where you left off. Load, continue, or delete workspaces from the sidebar.
""")

            st.markdown("#### 🔌 Data sources")
            st.markdown("""
- **CSV / Excel** — upload one or multiple files
- **Google Sheets** — paste a public sheet URL to pull live data
- **SQL database** — enter a SQLAlchemy connection string and a query to load results directly from PostgreSQL, MySQL, SQLite, and others
""")

            st.markdown("#### 📤 Export")
            st.markdown("""
- **Export HTML** — a self-contained report with all insights and interactive charts, ready to share
- **Export TXT** — plain-text conversation log
""")

        st.divider()
        st.markdown("#### Tips for better answers")
        st.markdown("""
| Do this | Instead of |
|---|---|
| *"Average order value by country"* | *"Tell me about orders"* |
| *"Top 5 categories by revenue, as a bar chart"* | *"Show me a chart"* |
| *"How has monthly revenue trended over 2024?"* | *"Show trends"* |
| *"What % of users churned in Q1?"* | *"Churn analysis"* |
""")
        st.info(
            "**Limitation:** Google Sheets must be shared as 'Anyone with the link can view'. "
            "SQL databases must be network-accessible from this machine."
        )


# ── Chat input ────────────────────────────────────────────────────────────────
question = st.chat_input("Ask a question about your data…")

if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

if question:
    if df is None:
        st.warning("Please load a dataset first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Analysing…"):
            try:
                schema = _schema()
                sample = get_sample(df)
                result, st.session_state.history = ask_question(
                    schema=schema,
                    sample=sample,
                    question=question,
                    history=st.session_state.history,
                    df=df,
                    datasets=st.session_state.datasets if len(st.session_state.datasets) > 1 else None,
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["insight"],
                    "stats": result.get("stats", []),
                    "chart": result.get("chart", {}),
                    "followups": result.get("followups", []),
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {e}",
                    "stats": [], "chart": {}, "followups": [],
                })
        st.rerun()
