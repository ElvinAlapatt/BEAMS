import random

import streamlit as st


st.set_page_config(
    page_title="BEAMS | Video analytics",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: var(--text-color);
        --muted: color-mix(in srgb, var(--text-color) 65%, var(--background-color));
        --line: color-mix(in srgb, var(--text-color) 14%, var(--background-color));
        --surface: var(--secondary-background-color);
        --canvas: var(--background-color);
        --green: var(--primary-color);
        --green-soft: color-mix(in srgb, var(--primary-color) 14%, var(--secondary-background-color));
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }
    h1, h2, h3, p, label { font-family: 'DM Sans', sans-serif; }

    .topline {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 0.75rem;
    }
    .brand-mark {
        display: inline-flex;
        width: 30px;
        height: 30px;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: var(--green);
        color: white;
        font-size: 0.8rem;
    }
    .hero-title {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 2.7rem);
        font-weight: 800;
        letter-spacing: -0.055em;
        line-height: 1.1;
        margin: 0;
    }
    .hero-copy {
        color: var(--muted);
        font-size: 1rem;
        margin: 0.6rem 0 1.6rem;
    }
    .section-heading {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 0.2rem;
    }
    .section-copy {
        color: var(--muted);
        font-size: 0.85rem;
        margin: 0 0 1rem;
    }
    .panel {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
    }
    .upload-panel {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 16px;
        min-height: 100%;
        padding: 1.25rem;
    }
    .eyebrow {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }
    .demo-pill {
        background: var(--green-soft);
        border-radius: 999px;
        color: var(--green);
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.35rem 0.65rem;
    }
    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1rem 1.1rem;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.8rem;
    }
    div[data-testid="stMetricValue"] {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: var(--surface);
        border: 1px dashed var(--line);
        border-radius: 12px;
    }
    [data-testid="stFileUploaderDropzone"] button {
        border: 1px solid var(--line);
        border-radius: 8px;
    }
    div[data-testid="stVideo"] {
        border-radius: 12px;
        overflow: hidden;
    }
    hr { border-color: var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topline">
        <span class="brand-mark">B</span>
        <span>BEAMS&nbsp; / &nbsp;VIDEO INTELLIGENCE</span>
    </div>
    <h1 class="hero-title">Video overview</h1>
    <p class="hero-copy">Upload a clip and explore your video insights in one place.</p>
    """,
    unsafe_allow_html=True,
)

upload_column, summary_column = st.columns([1.15, 0.85], gap="large")

with upload_column:
    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Your video</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Choose a video to add it to your workspace.</p>',
        unsafe_allow_html=True,
    )
    uploaded_video = st.file_uploader(
        "Upload video",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        help="Supported formats: MP4, MOV, AVI, MKV, and WebM.",
        label_visibility="collapsed",
    )
    if uploaded_video is not None:
        st.video(uploaded_video)
        st.caption(f"Selected video: {uploaded_video.name}")
    else:
        st.info("No video selected yet. Upload a clip to see its preview here.")
    st.markdown("</div>", unsafe_allow_html=True)

with summary_column:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="eyebrow">Workspace snapshot</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<span class="demo-pill">SAMPLE DATA</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "**Your video workspace is ready**  \n"
        "The metrics and charts below are illustrative placeholders. "
        "Connect your analysis pipeline to replace them with real results."
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-heading">Key metrics</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">A quick snapshot of sample video activity.</p>',
    unsafe_allow_html=True,
)

metric_columns = st.columns(4, gap="medium")
metrics = [
    ("Videos analyzed", "128", "+12.8%"),
    ("Avg. engagement", "74.6%", "+4.2%"),
    ("Events detected", "1,284", "+8.1%"),
    ("Processing time", "2.4 min", "-0.6 min"),
]
for column, (label, value, delta) in zip(metric_columns, metrics):
    column.metric(label, value, delta)

st.markdown("<br>", unsafe_allow_html=True)
chart_column, events_column = st.columns([1.45, 1], gap="large")

rng = random.Random(17)
hours = [f"{hour:02}:00" for hour in range(8, 20)]
activity = [
    max(12, 42 + index * 3 + rng.randint(-14, 14))
    for index in range(len(hours))
]
event_counts = [68, 52, 37, 24, 16]
event_names = ["People", "Objects", "Motion", "Scenes", "Other"]

with chart_column:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Activity over time</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Sample detections by hour</p>',
        unsafe_allow_html=True,
    )
    st.line_chart(
        {"Hour": hours, "Detections": activity},
        x="Hour",
        y="Detections",
        height=270,
        color="#1f8a68",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with events_column:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Event breakdown</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Example detections by category</p>',
        unsafe_allow_html=True,
    )
    st.bar_chart(
        {"Event": event_names, "Count": event_counts},
        x="Event",
        y="Count",
        height=270,
        color="#79bca3",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("BEAMS video analytics · Dashboard starter · Metrics shown are sample data.")