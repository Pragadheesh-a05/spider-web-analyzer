import streamlit as st
import cv2
import numpy as np
from PIL import Image
import base64

st.set_page_config(page_title="Spider Web Analyzer", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_background():
    try:
        with open("background.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

bg_img = load_background()
bg_style = f'url("data:image/png;base64,{bg_img}")' if bg_img else "linear-gradient(135deg, #0a0a0a 0%, #111827 100%)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    .stApp {{
        background-image: {bg_style};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'DM Mono', monospace;
    }}

    /* Hide all Streamlit chrome */
    #MainMenu, header, footer, .stDeployButton {{ display: none !important; }}
    .block-container {{ padding: 2rem 3rem !important; max-width: 1400px !important; }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: rgba(0,0,0,0.6);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.15);
        width: fit-content;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Syne', sans-serif;
        font-weight: 600;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.7) !important;
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 1.4rem !important;
        border-radius: 7px;
        transition: all 0.2s ease;
    }}
    .stTabs [aria-selected="true"] {{
        color: #fff !important;
        background: rgba(255,255,255,0.18) !important;
    }}

    /* Upload zone — dark transparent so all text is visible */
    [data-testid="stFileUploader"] {{
        background: rgba(0,0,0,0.55) !important;
        border: 1.5px dashed rgba(255,255,255,0.35) !important;
        border-radius: 14px !important;
        padding: 2rem !important;
        transition: border-color 0.3s ease;
        backdrop-filter: blur(6px) !important;
    }}
    [data-testid="stFileUploader"]:hover {{
        border-color: rgba(255,255,255,0.6) !important;
    }}
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploader"] div {{
        background: transparent !important;
    }}
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {{
        color: #ffffff !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        background: transparent !important;
    }}
    [data-testid="stFileUploader"] button {{
        background: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 8px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.78rem !important;
        padding: 0.4rem 1.2rem !important;
    }}
    [data-testid="stFileUploader"] button:hover {{
        background: rgba(255,255,255,0.28) !important;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        background: rgba(0,0,0,0.55) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        padding: 1.1rem 1.4rem !important;
        backdrop-filter: blur(8px) !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: 'DM Mono', monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.85) !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Syne', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
    }}

    /* Images */
    [data-testid="stImage"] img {{
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }}
    [data-testid="stImage"] p {{ display: none !important; }}

    /* Spinner */
    .stSpinner {{ color: rgba(255,255,255,0.5) !important; }}
    .stSpinner > div {{ border-top-color: white !important; }}

    /* Dividers */
    hr {{ border-color: rgba(255,255,255,0.08) !important; margin: 1.5rem 0 !important; }}

    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1,
    .stMarkdown h2, .stMarkdown h3, .stMarkdown td, .stMarkdown th {{
        color: #ffffff !important;
        font-family: 'DM Mono', monospace !important;
        text-shadow: 0 1px 6px rgba(0,0,0,0.95), 0 0 20px rgba(0,0,0,0.8);
    }}
    .stMarkdown h1 {{ font-family: 'Syne', sans-serif !important; font-size: 1.6rem !important; font-weight: 800 !important; color: #fff !important; }}
    .stMarkdown h2 {{ font-family: 'Syne', sans-serif !important; font-size: 1.1rem !important; font-weight: 700 !important; color: #ffffff !important; margin-top: 1.5rem !important; }}
    
    /* Wrap tab panel content in a dark overlay */
    [data-baseweb="tab-panel"] {{
        background: rgba(0,0,0,0.45) !important;
        border-radius: 14px !important;
        padding: 1.8rem 2rem !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }}

    /* Page heading */
    .page-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.9);
    }}
    .page-sub {{
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: #ffffff;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 2rem;
        text-shadow: 0 1px 6px rgba(0,0,0,0.8);
    }}

    /* Legend badges */
    .legend {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }}
    .badge {{
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
    }}
    .badge-c {{ background: rgba(255,60,60,0.15); color: #ff6b6b; border: 1px solid rgba(255,60,60,0.3); }}
    .badge-m {{ background: rgba(255,220,50,0.12); color: #ffd666; border: 1px solid rgba(255,220,50,0.25); }}
    .badge-f {{ background: rgba(80,160,255,0.15); color: #70b8ff; border: 1px solid rgba(80,160,255,0.3); }}
</style>

<div class="page-title">Spider Web Analyzer</div>
<div class="page-sub">Particle Detection &amp; Classification</div>
""", unsafe_allow_html=True)


def analyze_spider_web(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    orig = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    particles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 20 < area < 3000:
            x, y, w, h = cv2.boundingRect(cnt)
            diameter = np.sqrt(4 * area / np.pi)

            if diameter > 50:
                ptype, color = "COARSE", (60, 60, 255)
            elif diameter > 20:
                ptype, color = "MEDIUM", (50, 220, 255)
            else:
                ptype, color = "FINE", (255, 130, 70)

            particles.append({'size': round(diameter, 1), 'type': ptype})
            center = (x + w // 2, y + h // 2)
            cv2.circle(orig, center, int(diameter / 2), color, 2)
            cv2.putText(orig, ptype[0], (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    summary = {
        'total': len(particles),
        'coarse': len([p for p in particles if p['type'] == 'COARSE']),
        'medium': len([p for p in particles if p['type'] == 'MEDIUM']),
        'fine': len([p for p in particles if p['type'] == 'FINE']),
        'avg': round(np.mean([p['size'] for p in particles]), 1) if particles else 0
    }
    return summary, orig


tab1, tab2 = st.tabs(["Analyze", "About"])

with tab1:
    up_col, _, _ = st.columns([2, 1, 1])
    with up_col:
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)

        col_left, col_right = st.columns(2, gap="large")

        with col_left:
            st.image(image, use_column_width=True)

        with col_right:
            with st.spinner("Analyzing..."):
                results, viz_img = analyze_spider_web(image)

            c1, c2, c3 = st.columns(3)
            c1.metric("Coarse", results['coarse'])
            c2.metric("Medium", results['medium'])
            c3.metric("Fine", results['fine'])

            st.metric("Total", results['total'])
            st.metric("Avg Size", f"{results['avg']} px")

            st.markdown("""
            <div class="legend">
                <span class="badge badge-c">■ Coarse  &gt;50px</span>
                <span class="badge badge-m">■ Medium  20–50px</span>
                <span class="badge badge-f">■ Fine  &lt;20px</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.image(cv2.cvtColor(viz_img, cv2.COLOR_BGR2RGB), use_column_width=True)

with tab2:
    st.markdown("""
# About This Tool

Upload a spider web image and the system automatically detects and measures particles trapped within the web structure — no manual inspection required.

## How It Works

Particle contours are isolated using adaptive thresholding and analyzed via OpenCV. Each detected particle is measured and automatically classified based on its estimated diameter.

## Who Is It For

Built for chemical engineers, environmental researchers, and material scientists — this tool bridges image analysis with practical particle distribution insights, supporting work in filtration studies, air quality monitoring, and materials characterization.

""")
