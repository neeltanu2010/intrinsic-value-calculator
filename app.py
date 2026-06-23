import math
from datetime import datetime
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =====================================================
# FINANCIFY - FREE INTRINSIC VALUE CALCULATOR
# Premium hook tool for Financify blog
# =====================================================

st.set_page_config(
    page_title="Financify Intrinsic Value Calculator",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="auto",
)

SURECART_CHECKOUT_URL = "https://financify.blog/buy/financify-tools"
TOOLS_PAGE_URL = "https://financify.blog/tools"
BLOG_URL = "https://financify.blog"

# Mobile-friendly Plotly config
PLOTLY_MOBILE_CONFIG = {"responsive": True, "displayModeBar": False}


# Plot readability safety patch
# Keeps charts readable on mobile and desktop even when Streamlit/theme CSS tries to make plot text white.
def apply_financify_plot_theme(fig):
    try:
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Inter, Arial, sans-serif", size=13, color="#111111"),
            title=dict(font=dict(color="#111111", size=18), x=0.02, xanchor="left"),
            legend=dict(
                font=dict(color="#111111", size=12),
                bgcolor="rgba(255,255,255,0.88)",
                bordercolor="rgba(17,17,17,0.10)",
                borderwidth=1,
            ),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            hoverlabel=dict(
                bgcolor="#111111",
                bordercolor="#FFD21F",
                font=dict(color="#FFD21F", family="Inter, Arial, sans-serif", size=12),
            ),
        )
        fig.update_xaxes(
            title_font=dict(color="#111111", size=13),
            tickfont=dict(color="#111111", size=11),
            gridcolor="rgba(17,17,17,0.10)",
            zerolinecolor="rgba(17,17,17,0.18)",
            linecolor="rgba(17,17,17,0.18)",
            automargin=True,
        )
        fig.update_yaxes(
            title_font=dict(color="#111111", size=13),
            tickfont=dict(color="#111111", size=11),
            gridcolor="rgba(17,17,17,0.10)",
            zerolinecolor="rgba(17,17,17,0.18)",
            linecolor="rgba(17,17,17,0.18)",
            automargin=True,
        )
        fig.update_layout(
            polar=dict(
                bgcolor="#ffffff",
                radialaxis=dict(
                    tickfont=dict(color="#111111", size=10),
                    title_font=dict(color="#111111", size=12),
                    gridcolor="rgba(17,17,17,0.16)",
                    linecolor="rgba(17,17,17,0.20)",
                ),
                angularaxis=dict(
                    tickfont=dict(color="#111111", size=11),
                    gridcolor="rgba(17,17,17,0.16)",
                    linecolor="rgba(17,17,17,0.20)",
                ),
            )
        )
        fig.update_traces(textfont=dict(color="#111111", size=12), selector=dict(type="bar"))
        fig.update_traces(textfont=dict(color="#111111", size=12), selector=dict(type="pie"))
        fig.update_traces(insidetextfont=dict(color="#111111", size=12), outsidetextfont=dict(color="#111111", size=12), selector=dict(type="pie"))
        fig.update_traces(textfont=dict(color="#111111", size=12), selector=dict(type="heatmap"))
        fig.update_traces(number=dict(font=dict(color="#111111", size=28)), title=dict(font=dict(color="#111111", size=14)), selector=dict(type="indicator"))
    except Exception:
        pass
    return fig


if not hasattr(st, "_financify_original_plotly_chart"):
    st._financify_original_plotly_chart = st.plotly_chart


def _financify_safe_plotly_chart(fig_or_data, *args, **kwargs):
    try:
        if hasattr(fig_or_data, "update_layout"):
            fig_or_data = apply_financify_plot_theme(fig_or_data)
    except Exception:
        pass
    return st._financify_original_plotly_chart(fig_or_data, *args, **kwargs)


st.plotly_chart = _financify_safe_plotly_chart

# -------------------------
# Premium CSS
# -------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 210, 31, 0.20), transparent 32%),
            radial-gradient(circle at bottom right, rgba(255, 210, 31, 0.12), transparent 30%),
            linear-gradient(135deg, #fffaf0 0%, #fff8dc 42%, #fffdf5 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.13;
        background-image:
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(60deg, rgba(0,0,0,0.18) 25%, transparent 25.5%, transparent 75%, rgba(0,0,0,0.18) 75%, rgba(0,0,0,0.18));
        background-size: 58px 102px;
        background-position: 0 0, 0 0, 29px 51px, 29px 51px, 0 0;
        z-index: -1;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #171100 100%);
        border-right: 1px solid rgba(255, 210, 31, 0.25);
    }

    section[data-testid="stSidebar"] * {
        color: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #111 !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #050505 0%, #171100 55%, #3a2b00 100%);
        border: 1px solid rgba(255, 210, 31, 0.55);
        border-radius: 28px;
        padding: 34px 34px 30px 34px;
        box-shadow: 0 24px 80px rgba(0,0,0,0.22);
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        inset: -2px;
        background: radial-gradient(circle at 88% 18%, rgba(255,210,31,0.32), transparent 24%);
        pointer-events: none;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 210, 31, 0.15);
        color: #ffe680;
        border: 1px solid rgba(255, 210, 31, 0.45);
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(2.05rem, 4vw, 4rem);
        line-height: 1.02;
        font-weight: 950;
        letter-spacing: -0.055em;
        margin-top: 18px;
        margin-bottom: 16px;
        max-width: 880px;
    }

    .hero-title span {
        color: #FFD21F;
    }

    .hero-subtitle {
        color: #fff4bd;
        font-size: 1.04rem;
        line-height: 1.7;
        max-width: 850px;
        margin-bottom: 20px;
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }

    .pill {
        background: rgba(255, 255, 255, 0.08);
        color: #fff7cf;
        border: 1px solid rgba(255, 210, 31, 0.28);
        border-radius: 999px;
        padding: 9px 13px;
        font-size: 0.88rem;
        font-weight: 750;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 14px 42px rgba(20, 14, 0, 0.08);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(180deg, #ffffff 0%, #fff8d8 100%);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 12px 28px rgba(17, 17, 17, 0.08);
        min-height: 140px;
    }

    .metric-label {
        color: #5c4a00;
        font-size: 0.86rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #080808;
        font-size: 1.75rem;
        font-weight: 950;
        letter-spacing: -0.035em;
        margin-bottom: 6px;
    }

    .metric-help {
        color: #5a5a5a;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 950;
        color: #111;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #5b5b5b;
        font-size: 0.97rem;
        line-height: 1.55;
        margin-bottom: 18px;
    }

    .verdict-box {
        border-radius: 26px;
        padding: 24px;
        color: #fffdf0;
        border: 1px solid rgba(255, 210, 31, 0.44);
        box-shadow: 0 18px 42px rgba(0,0,0,0.20);
        background: linear-gradient(135deg, #090909 0%, #241a00 62%, #514000 100%);
    }

    .verdict-title {
        font-size: 1.42rem;
        font-weight: 950;
        color: #FFD21F;
        margin-bottom: 8px;
    }

    .verdict-text {
        color: #fff7cf;
        font-size: 1rem;
        line-height: 1.65;
    }

    .mini-badge {
        display: inline-block;
        background: #FFD21F;
        color: #111;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 950;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .warning-box {
        background: #fff2bd;
        border-left: 6px solid #FFD21F;
        border-radius: 18px;
        padding: 16px 18px;
        color: #2f2600;
        line-height: 1.58;
        font-weight: 600;
    }

    .cta-card {
        background: linear-gradient(135deg, #FFD21F 0%, #ffb800 100%);
        color: #111;
        border-radius: 26px;
        padding: 25px;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 18px 40px rgba(122, 91, 0, 0.18);
    }

    .cta-card h3 {
        color: #111;
        font-size: 1.55rem;
        font-weight: 950;
        margin-bottom: 8px;
        letter-spacing: -0.035em;
    }

    .cta-card p {
        color: #241b00;
        line-height: 1.58;
        font-weight: 600;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 999px !important;
        border: 1px solid rgba(17,17,17,0.13) !important;
        background: linear-gradient(135deg, #111 0%, #2a2100 100%) !important;
        color: #FFD21F !important;
        font-weight: 900 !important;
        padding: 0.72rem 1.1rem !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 20px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    div[data-testid="stTabs"] button {
        font-weight: 850;
    }

    .footer-note {
        color: #6b5d27;
        text-align: center;
        font-size: 0.86rem;
        margin-top: 24px;
    }

    @media (max-width: 768px) {
        .hero-card { padding: 26px 20px; border-radius: 22px; }
        .glass-card { padding: 18px; border-radius: 20px; }
        .metric-value { font-size: 1.45rem; }
    }


    /* =====================================================
       FINANCIFY MOBILE + READABILITY PATCH
       Keeps the original theme, fixes mobile overflow and invisible text.
       ===================================================== */
    :root { color-scheme: light; }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        -webkit-text-size-adjust: 100%;
        text-rendering: optimizeLegibility;
    }

    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    .main .block-container,
    [data-testid="stAppViewContainer"] .block-container {
        width: 100% !important;
        max-width: min(1260px, 100%) !important;
        padding-left: clamp(0.90rem, 3.2vw, 2.00rem) !important;
        padding-right: clamp(0.90rem, 3.2vw, 2.00rem) !important;
    }

    .block-container p,
    .block-container li,
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4,
    .block-container h5,
    .block-container h6,
    .block-container span,
    .hero-title,
    .hero-subtitle,
    .section-title,
    .section-subtitle,
    .metric-label,
    .metric-value,
    .metric-help,
    .verdict-title,
    .verdict-text,
    .light-text,
    .pill,
    .mini-badge,
    .soft-badge {
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    .hero-card,
    .glass-card,
    .dark-card,
    .metric-card,
    .verdict-box,
    .warning-box,
    .danger-box,
    .cta-card {
        max-width: 100% !important;
        isolation: isolate;
    }

    .hero-card > *,
    .dark-card > *,
    .verdict-box > * {
        position: relative;
        z-index: 1;
    }

    .glass-card,
    .metric-card,
    .warning-box,
    .danger-box,
    .cta-card {
        color: #111111 !important;
    }

    .glass-card p,
    .glass-card li,
    .glass-card span,
    .metric-card p,
    .metric-card li,
    .warning-box p,
    .warning-box li,
    .danger-box p,
    .danger-box li,
    .cta-card p,
    .cta-card li {
        opacity: 1 !important;
    }

    .dark-card,
    .dark-card p,
    .dark-card li,
    .dark-card span,
    .verdict-box,
    .verdict-box p,
    .verdict-box li,
    .verdict-box span,
    .hero-card,
    .hero-card p,
    .hero-card li,
    .hero-card span {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .hero-title,
    .hero-title span,
    .verdict-title,
    .section-title-light {
        -webkit-text-fill-color: currentColor !important;
    }

    .metric-label { color: #5c4a00 !important; }
    .metric-value { color: #070707 !important; }
    .metric-help { color: #4c4c4c !important; }
    .section-title { color: #111111 !important; }
    .section-subtitle { color: #4d4d4d !important; }
    .warning-box, .warning-box * { color: #2f2600 !important; -webkit-text-fill-color: #2f2600 !important; }
    .danger-box, .danger-box * { color: #3b120a !important; -webkit-text-fill-color: #3b120a !important; }
    .cta-card, .cta-card * { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

    /* Sidebar: readable labels on dark background, readable input text on light fields.
       Width is left to Streamlit default so desktop stays normal and mobile fully collapses. */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #fff8d8 !important;
        -webkit-text-fill-color: #fff8d8 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="input"] input,
    section[data-testid="stSidebar"] [data-baseweb="textarea"] textarea,
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: #fffaf0 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        border: 1px solid rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
        background: #fffaf0 !important;
        color: #111111 !important;
        border-color: rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="menu"] [role="option"] {
        background: #fffaf0 !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        font-size: 16px !important;
    }

    /* Tables and Plotly should scroll/resize instead of cutting text on phones. */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    .stDataFrame,
    .stTable {
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 16px !important;
    }

    div[data-testid="stDataFrame"] * {
        font-size: clamp(0.74rem, 2.9vw, 0.92rem) !important;
    }

    .js-plotly-plot,
    .plotly,
    .plot-container,
    div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        gap: 0.35rem !important;
        scrollbar-width: none;
    }

    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        display: none;
    }

    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button p {
        white-space: nowrap !important;
        font-size: clamp(0.78rem, 3.1vw, 0.94rem) !important;
        line-height: 1.2 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.75rem !important;
            padding-bottom: 2rem !important;
        }

        .hero-card {
            padding: 1.25rem 1rem !important;
            border-radius: 21px !important;
            margin-bottom: 1rem !important;
        }

        .hero-title {
            font-size: clamp(1.72rem, 9vw, 2.35rem) !important;
            letter-spacing: -0.038em !important;
            line-height: 1.07 !important;
            margin-top: 0.95rem !important;
            margin-bottom: 0.75rem !important;
        }

        .hero-subtitle {
            font-size: 0.96rem !important;
            line-height: 1.55 !important;
            margin-bottom: 0.85rem !important;
        }

        .hero-pills {
            gap: 0.45rem !important;
            margin-top: 0.85rem !important;
        }

        .pill,
        .mini-badge,
        .soft-badge {
            font-size: 0.76rem !important;
            line-height: 1.2 !important;
            padding: 0.45rem 0.62rem !important;
        }

        .glass-card,
        .dark-card,
        .metric-card,
        .verdict-box,
        .warning-box,
        .danger-box,
        .cta-card {
            padding: 1rem !important;
            border-radius: 18px !important;
            margin-bottom: 0.95rem !important;
        }

        .metric-card {
            min-height: auto !important;
        }

        .metric-label {
            font-size: 0.73rem !important;
            line-height: 1.18 !important;
            letter-spacing: 0.045em !important;
        }

        .metric-value {
            font-size: clamp(1.15rem, 6.2vw, 1.55rem) !important;
            line-height: 1.13 !important;
        }

        .metric-help,
        .section-subtitle,
        .verdict-text,
        .light-text {
            font-size: 0.91rem !important;
            line-height: 1.50 !important;
        }

        .section-title,
        .section-title-light,
        .verdict-title {
            font-size: 1.18rem !important;
            line-height: 1.20 !important;
            letter-spacing: -0.025em !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            padding: 0.75rem 0.95rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetric"] {
            padding: 0.85rem 0.9rem !important;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
            font-size: 0.76rem !important;
            white-space: normal !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
            line-height: 1.15 !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stPlotlyChart"] {
            border-radius: 16px !important;
        }

        iframe,
        img,
        video,
        canvas,
        svg {
            max-width: 100% !important;
        }
    }

    @media (max-width: 420px) {
        .hero-title {
            font-size: clamp(1.58rem, 10vw, 2.05rem) !important;
        }

        .eyebrow {
            font-size: 0.74rem !important;
            padding: 0.43rem 0.58rem !important;
        }

        .metric-value {
            font-size: clamp(1.05rem, 7vw, 1.35rem) !important;
        }

        .block-container {
            padding-left: 0.72rem !important;
            padding-right: 0.72rem !important;
        }
    }



    /* =====================================================
       FINANCIFY MAIN PAGE TEXT COLOR SAFETY PATCH
       Fixes washed/white text on mobile light background without changing logic.
       ===================================================== */
    [data-testid="stAppViewContainer"] .main .block-container,
    [data-testid="stAppViewContainer"] .main .block-container *:not(svg):not(path):not(rect):not(circle):not(line):not(polyline):not(polygon) {
        opacity: 1 !important;
        text-shadow: none !important;
    }

    [data-testid="stAppViewContainer"] .main .block-container,
    [data-testid="stAppViewContainer"] .main .block-container p,
    [data-testid="stAppViewContainer"] .main .block-container li,
    [data-testid="stAppViewContainer"] .main .block-container span,
    [data-testid="stAppViewContainer"] .main .block-container div,
    [data-testid="stAppViewContainer"] .main .block-container label,
    [data-testid="stAppViewContainer"] .main .block-container small,
    [data-testid="stAppViewContainer"] .main .block-container strong,
    [data-testid="stAppViewContainer"] .main .block-container em,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    .section-title,
    .section-subtitle,
    .metric-label,
    .metric-value,
    .metric-help,
    .footer-note {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    .glass-card,
    .glass-card *:not(svg):not(path),
    .metric-card,
    .metric-card *:not(svg):not(path),
    .warning-box,
    .warning-box *:not(svg):not(path),
    .danger-box,
    .danger-box *:not(svg):not(path),
    .cta-card,
    .cta-card *:not(svg):not(path) {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    .hero-card,
    .hero-card *:not(svg):not(path),
    .dark-card,
    .dark-card *:not(svg):not(path),
    .verdict-box,
    .verdict-box *:not(svg):not(path) {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .hero-title,
    .hero-title *:not(svg):not(path) {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .hero-title span,
    .eyebrow,
    .eyebrow *:not(svg):not(path),
    .verdict-title,
    .section-title-light,
    .dark-card .section-title-light,
    .dark-card .verdict-title,
    .verdict-box .verdict-title {
        color: #FFD21F !important;
        -webkit-text-fill-color: #FFD21F !important;
    }

    .pill,
    .pill *:not(svg):not(path),
    .soft-badge,
    .soft-badge *:not(svg):not(path) {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .glass-card .soft-badge,
    .glass-card .soft-badge *:not(svg):not(path),
    .metric-card .soft-badge,
    .metric-card .soft-badge *:not(svg):not(path) {
        color: #3a2c00 !important;
        -webkit-text-fill-color: #3a2c00 !important;
    }

    .mini-badge,
    .mini-badge *:not(svg):not(path),
    .danger-badge,
    .danger-badge *:not(svg):not(path) {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    .metric-label { color: #5c4a00 !important; -webkit-text-fill-color: #5c4a00 !important; }
    .metric-value { color: #070707 !important; -webkit-text-fill-color: #070707 !important; }
    .metric-help { color: #4c4c4c !important; -webkit-text-fill-color: #4c4c4c !important; }
    .section-title { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }
    .section-subtitle { color: #4d4d4d !important; -webkit-text-fill-color: #4d4d4d !important; }
    .warning-box, .warning-box *:not(svg):not(path) { color: #2f2600 !important; -webkit-text-fill-color: #2f2600 !important; }
    .danger-box, .danger-box *:not(svg):not(path) { color: #3b120a !important; -webkit-text-fill-color: #3b120a !important; }
    .cta-card, .cta-card *:not(svg):not(path) { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

    a,
    [data-testid="stMarkdownContainer"] a {
        color: #6f4f00 !important;
        -webkit-text-fill-color: #6f4f00 !important;
        font-weight: 850 !important;
    }

    .hero-card a,
    .dark-card a,
    .verdict-box a,
    .hero-card a *:not(svg):not(path),
    .dark-card a *:not(svg):not(path),
    .verdict-box a *:not(svg):not(path) {
        color: #FFD21F !important;
        -webkit-text-fill-color: #FFD21F !important;
    }

    div[data-testid="stMetric"],
    div[data-testid="stMetric"] *:not(svg):not(path) {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        opacity: 1 !important;
    }

    .stAlert,
    .stAlert *:not(svg):not(path) {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        opacity: 1 !important;
    }

    @media (max-width: 768px) {
        [data-testid="stAppViewContainer"] .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container > div,
        [data-testid="stAppViewContainer"] .main .block-container p,
        [data-testid="stAppViewContainer"] .main .block-container li,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stWidgetLabel"] * {
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
            opacity: 1 !important;
        }

        .hero-card,
        .hero-card *:not(svg):not(path),
        .dark-card,
        .dark-card *:not(svg):not(path),
        .verdict-box,
        .verdict-box *:not(svg):not(path) {
            color: #fff7cf !important;
            -webkit-text-fill-color: #fff7cf !important;
        }

        .hero-title,
        .hero-title *:not(svg):not(path) {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        .hero-title span,
        .eyebrow,
        .eyebrow *:not(svg):not(path),
        .verdict-title,
        .section-title-light,
        .dark-card .section-title-light,
        .verdict-box .verdict-title {
            color: #FFD21F !important;
            -webkit-text-fill-color: #FFD21F !important;
        }

        .glass-card,
        .glass-card *:not(svg):not(path),
        .metric-card,
        .metric-card *:not(svg):not(path),
        .warning-box,
        .warning-box *:not(svg):not(path),
        .danger-box,
        .danger-box *:not(svg):not(path),
        .cta-card,
        .cta-card *:not(svg):not(path) {
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
            opacity: 1 !important;
        }
    }



    /* Plot readability fix */
    div[data-testid="stPlotlyChart"],
    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        background: #ffffff !important;
        border-radius: 18px !important;
        overflow: visible !important;
    }

    div[data-testid="stPlotlyChart"] svg text {
        fill: #111111 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stPlotlyChart"] .legend text,
    div[data-testid="stPlotlyChart"] .gtitle,
    div[data-testid="stPlotlyChart"] .xtick text,
    div[data-testid="stPlotlyChart"] .ytick text,
    div[data-testid="stPlotlyChart"] .xaxislayer-above text,
    div[data-testid="stPlotlyChart"] .yaxislayer-above text,
    div[data-testid="stPlotlyChart"] .annotation-text,
    div[data-testid="stPlotlyChart"] .slicetext {
        fill: #111111 !important;
        color: #111111 !important;
        text-shadow: none !important;
    }

    @media (max-width: 768px) {
        div[data-testid="stPlotlyChart"] {
            min-height: 320px !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.8rem !important;
        }
        div[data-testid="stPlotlyChart"] svg text {
            font-size: 11px !important;
        }
        div[data-testid="stPlotlyChart"] .gtitle {
            font-size: 14px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Calculation helpers
# -------------------------

def safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def money(x):
    if x is None or not np.isfinite(x):
        return "—"
    return f"₹{x:,.2f}"


def pct(x):
    if x is None or not np.isfinite(x):
        return "—"
    return f"{x * 100:.2f}%"


def calculate_value(base_metric, growth, years, exit_multiple, discount_rate, margin_of_safety):
    """EPS/FCF multiple based fair value model."""
    if base_metric <= 0 or years <= 0 or exit_multiple <= 0 or discount_rate <= -0.99:
        return {
            "future_metric": np.nan,
            "future_exit_value": np.nan,
            "fair_value": np.nan,
            "mos_price": np.nan,
        }

    future_metric = base_metric * ((1 + growth) ** years)
    future_exit_value = future_metric * exit_multiple
    fair_value = future_exit_value / ((1 + discount_rate) ** years)
    mos_price = fair_value * (1 - margin_of_safety)

    return {
        "future_metric": future_metric,
        "future_exit_value": future_exit_value,
        "fair_value": fair_value,
        "mos_price": mos_price,
    }


def reverse_implied_growth(current_price, base_metric, years, exit_multiple, discount_rate):
    if current_price <= 0 or base_metric <= 0 or years <= 0 or exit_multiple <= 0 or discount_rate <= -0.99:
        return np.nan
    try:
        implied = ((current_price * ((1 + discount_rate) ** years)) / (base_metric * exit_multiple)) ** (1 / years) - 1
        return implied
    except Exception:
        return np.nan


def assumption_score(growth, discount_rate, exit_multiple, margin_of_safety, years, metric_type):
    score = 0
    notes = []

    if growth <= 0.08:
        score += 22
        notes.append("Growth assumption looks conservative.")
    elif growth <= 0.14:
        score += 16
        notes.append("Growth assumption is reasonable but needs business quality support.")
    elif growth <= 0.20:
        score += 9
        notes.append("Growth assumption is aggressive; check durability carefully.")
    else:
        score += 3
        notes.append("Growth assumption is very aggressive; the bee is flying close to the candle.")

    if 0.10 <= discount_rate <= 0.15:
        score += 22
        notes.append("Discount rate gives a decent return hurdle.")
    elif 0.08 <= discount_rate < 0.10 or 0.15 < discount_rate <= 0.18:
        score += 14
        notes.append("Discount rate is usable, but sensitivity matters.")
    else:
        score += 6
        notes.append("Discount rate may be too low or too high for a practical estimate.")

    if exit_multiple <= 18:
        score += 18
        notes.append("Exit multiple is conservative.")
    elif exit_multiple <= 28:
        score += 13
        notes.append("Exit multiple is acceptable for a quality business.")
    elif exit_multiple <= 40:
        score += 7
        notes.append("Exit multiple is rich; the company must truly deserve it.")
    else:
        score += 2
        notes.append("Exit multiple is very rich; valuation risk is high.")

    if margin_of_safety >= 0.30:
        score += 18
        notes.append("Margin of safety is strong.")
    elif margin_of_safety >= 0.20:
        score += 14
        notes.append("Margin of safety is decent.")
    elif margin_of_safety >= 0.10:
        score += 8
        notes.append("Margin of safety is thin.")
    else:
        score += 2
        notes.append("Margin of safety is too low for uncertain estimates.")

    if years >= 7:
        score += 12
        notes.append("Time horizon is long enough for compounding to show up.")
    elif years >= 5:
        score += 8
        notes.append("Time horizon is acceptable.")
    else:
        score += 3
        notes.append("Short time horizon can make intrinsic value noisy.")

    if "Owner" in metric_type or "FCF" in metric_type:
        score += 8
        notes.append("Cash-flow based valuation is usually cleaner than accounting EPS alone.")
    else:
        score += 5
        notes.append("EPS works, but confirm with CFO and FCF quality.")

    return min(score, 100), notes


def get_verdict(current_price, base_fair, base_mos, bear_fair, bull_fair):
    if not np.isfinite(base_fair) or not np.isfinite(base_mos):
        return "Need cleaner inputs", "Enter positive values for metric, growth, years, multiple and discount rate."

    if current_price <= 0:
        return "Fair value estimated", "Add current market price to compare valuation zones and calculate upside/downside."

    if current_price <= base_mos:
        return "Honey Zone 🐝", "The current price is below your margin-of-safety price based on these assumptions. Still verify business quality before celebrating."
    if current_price <= bear_fair:
        return "Conservative Watch Zone 🍯", "The price is near or below conservative value. This may be interesting if the business quality is strong."
    if current_price <= base_fair:
        return "Reasonable Zone ✅", "The price is below base fair value, but not necessarily a bargain. Margin of safety matters."
    if np.isfinite(bull_fair) and current_price <= bull_fair:
        return "Optimism Priced In ⚠️", "The stock needs bullish assumptions to look attractive. Be careful with growth and exit multiple."
    return "Bubble Smell Zone 🫧", "The price is above even the bullish estimate. That does not mean sell, but it means expectations are already flying high."


def make_value_chart(company, current_price, rows):
    labels = []
    values = []

    if current_price > 0:
        labels.append("Current Price")
        values.append(current_price)

    for _, row in rows.iterrows():
        labels.append(f"{row['Case']} Fair Value")
        values.append(row["Fair Value"])
        if row["Case"] == "Base":
            labels.append("Base MOS Price")
            values.append(row["MOS Price"])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            text=[money(v) for v in values],
            textposition="outside",
            hovertemplate="%{x}<br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"{company or 'Stock'} valuation map",
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=50),
        yaxis_title="Value per share",
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_sensitivity_heatmap(base_metric, years, exit_multiple, margin_of_safety, growth, discount_rate):
    growth_points = np.array([growth - 0.04, growth - 0.02, growth, growth + 0.02, growth + 0.04])
    growth_points = np.maximum(growth_points, -0.30)
    discount_points = np.array([discount_rate - 0.03, discount_rate - 0.015, discount_rate, discount_rate + 0.015, discount_rate + 0.03])
    discount_points = np.maximum(discount_points, 0.01)

    z = []
    for d in discount_points:
        row = []
        for g in growth_points:
            calc = calculate_value(base_metric, g, years, exit_multiple, d, margin_of_safety)
            row.append(calc["fair_value"])
        z.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=[f"{g*100:.1f}%" for g in growth_points],
            y=[f"{d*100:.1f}%" for d in discount_points],
            text=[[money(v) for v in row] for row in z],
            texttemplate="%{text}",
            hovertemplate="Growth: %{x}<br>Discount: %{y}<br>Fair Value: %{text}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Sensitivity: growth rate vs discount rate",
        xaxis_title="Growth assumption",
        yaxis_title="Discount rate",
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def build_report(company, metric_type, base_metric, current_price, years, growth, discount_rate, exit_multiple, mos, rows, verdict_title, verdict_text, implied_growth, score, notes):
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    text = f"""
FINANCIFY INTRINSIC VALUE MINI REPORT
Generated: {generated}

Company/Stock: {company or 'Not specified'}
Metric used: {metric_type}
Current price entered: {money(current_price) if current_price > 0 else 'Not entered'}
Base metric per share: {money(base_metric)}
Time horizon: {years} years
Base growth: {growth*100:.2f}%
Discount rate: {discount_rate*100:.2f}%
Exit multiple: {exit_multiple:.2f}x
Margin of safety: {mos*100:.2f}%

VALUATION CASES
{rows.to_string(index=False)}

FINANCIFY VERDICT
{verdict_title}
{verdict_text}

Reverse implied growth at current price: {pct(implied_growth)}
Assumption quality score: {score}/100

ASSUMPTION NOTES
- """ + "\n- ".join(notes) + """

Educational disclaimer: This tool is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. Please do your own research or consult a SEBI-registered investment adviser before making decisions.
"""
    return text.strip()


def build_seo_draft(company, metric_type, base_metric, current_price, years, growth, discount_rate, exit_multiple, mos, base_fair, base_mos):
    stock_name = company.strip() if company.strip() else "This Stock"
    title = f"{stock_name} Intrinsic Value Calculator: Estimate Fair Value with Margin of Safety"
    meta = f"Use this free intrinsic value calculator to estimate {stock_name}'s fair value using growth, discount rate, exit multiple and margin of safety assumptions."
    excerpt = f"Estimate {stock_name}'s intrinsic value using a simple investor-style model. Change growth, discount rate and margin of safety to understand valuation risk before making decisions."

    body = f"""
# {title}

Many beginner investors look only at stock price. But price alone tells very little. A ₹500 stock can be expensive and a ₹5,000 stock can be reasonable depending on earnings, cash flow, growth and business quality.

This free Financify calculator estimates intrinsic value using a simple long-term valuation model. It uses your chosen base metric, growth assumption, exit multiple, discount rate and margin of safety.

## Inputs Used

- Metric used: {metric_type}
- Base metric per share: {money(base_metric)}
- Current price: {money(current_price) if current_price > 0 else 'Not entered'}
- Growth assumption: {growth*100:.2f}%
- Time horizon: {years} years
- Exit multiple: {exit_multiple:.2f}x
- Discount rate: {discount_rate*100:.2f}%
- Margin of safety: {mos*100:.2f}%

## Estimated Result

Based on these assumptions, the estimated fair value is around {money(base_fair)} per share. After applying margin of safety, the preferred safety price is around {money(base_mos)} per share.

## How to Read This

Intrinsic value is not a fixed magic number. It is a range based on assumptions. If growth is reduced or discount rate is increased, fair value can fall quickly. That is why a margin of safety is important.

## What Financify Suggests Checking Next

Before trusting any valuation number, check whether the business has durable quality. Look at debt, profit margin trend, ROE, ROCE, CFO, FCF, EPS growth and valuation comfort.

You can use Financify's advanced tools to check these factors faster.

## Disclaimer

This article and calculator are for educational purposes only. They are not investment advice, stock recommendations, or buy/sell signals. Please do your own research or consult a SEBI-registered investment adviser before investing.
""".strip()

    return title, meta, excerpt, body


# -------------------------
# Sidebar inputs
# -------------------------
with st.sidebar:
    st.markdown("### 🐝 Financify Inputs")
    st.caption("Use conservative assumptions. Fancy growth assumptions can make even weak stocks look like honey.")

    company = st.text_input("Company / Stock name", value="Example Stock")

    metric_type = st.selectbox(
        "Valuation base metric",
        [
            "EPS per share",
            "Owner Earnings per share",
            "Free Cash Flow per share",
        ],
        index=0,
        help="EPS is beginner-friendly. Owner earnings or FCF per share is often better for serious valuation.",
    )

    base_metric = st.number_input(
        "Latest EPS / FCF per share",
        min_value=0.01,
        value=50.0,
        step=1.0,
        help="Enter per-share number. Example: EPS of ₹50 or FCF per share of ₹50.",
    )

    current_price = st.number_input(
        "Current market price per share optional",
        min_value=0.0,
        value=900.0,
        step=10.0,
        help="Used only for comparison, upside/downside and reverse implied growth.",
    )

    st.divider()
    st.markdown("### Assumptions")

    years = st.slider("Projection period years", min_value=3, max_value=15, value=10, step=1)
    growth = st.slider("Expected annual growth", min_value=-10.0, max_value=35.0, value=10.0, step=0.5) / 100
    discount_rate = st.slider("Discount rate / required return", min_value=5.0, max_value=25.0, value=12.0, step=0.5) / 100
    exit_multiple = st.slider("Exit PE / cash-flow multiple", min_value=5.0, max_value=60.0, value=20.0, step=0.5)
    margin_of_safety = st.slider("Margin of safety", min_value=0.0, max_value=60.0, value=25.0, step=1.0) / 100

    st.divider()
    st.markdown("### Scenario settings")
    bear_growth_cut = st.slider("Bear case growth cut", 20, 80, 45, 5, help="45 means bear growth is 55% of base growth.") / 100
    bull_growth_boost = st.slider("Bull case growth boost", 5, 50, 20, 5, help="20 means bull growth is 20% higher than base growth.") / 100

    st.markdown("---")
    st.markdown(f"[🔓 Upgrade to Financify Pro]({SURECART_CHECKOUT_URL})")
    st.markdown(f"[🧰 Explore all tools]({TOOLS_PAGE_URL})")

# -------------------------
# Hero
# -------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">🐝 Free Financify Tool • Madness of Money Bees</div>
        <div class="hero-title">Intrinsic Value Calculator with <span>Margin of Safety</span></div>
        <div class="hero-subtitle">
            Estimate a stock's fair value using growth, discount rate and exit multiple. Then see a bear/base/bull valuation map,
            reverse implied growth, assumption quality score, and a Warren-style checklist — without pretending valuation is magic.
        </div>
        <div class="hero-pills">
            <div class="pill">Bear/Base/Bull Cases</div>
            <div class="pill">Reverse DCF Growth</div>
            <div class="pill">Margin of Safety Zone</div>
            <div class="pill">Financify Bee Verdict</div>
            <div class="pill">SEO Article Draft</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Calculations
# -------------------------
bear_growth = growth * (1 - bear_growth_cut)
bull_growth = growth * (1 + bull_growth_boost)

cases = [
    {
        "Case": "Bear",
        "Growth": bear_growth,
        "Discount Rate": discount_rate + 0.015,
        "Exit Multiple": max(3.0, exit_multiple * 0.85),
    },
    {
        "Case": "Base",
        "Growth": growth,
        "Discount Rate": discount_rate,
        "Exit Multiple": exit_multiple,
    },
    {
        "Case": "Bull",
        "Growth": bull_growth,
        "Discount Rate": max(0.01, discount_rate - 0.01),
        "Exit Multiple": exit_multiple * 1.15,
    },
]

rows = []
for item in cases:
    calc = calculate_value(
        base_metric=base_metric,
        growth=item["Growth"],
        years=years,
        exit_multiple=item["Exit Multiple"],
        discount_rate=item["Discount Rate"],
        margin_of_safety=margin_of_safety,
    )
    rows.append(
        {
            "Case": item["Case"],
            "Growth": item["Growth"],
            "Discount Rate": item["Discount Rate"],
            "Exit Multiple": item["Exit Multiple"],
            "Future Metric": calc["future_metric"],
            "Fair Value": calc["fair_value"],
            "MOS Price": calc["mos_price"],
        }
    )

valuation_df = pd.DataFrame(rows)
base_row = valuation_df[valuation_df["Case"] == "Base"].iloc[0]
bear_row = valuation_df[valuation_df["Case"] == "Bear"].iloc[0]
bull_row = valuation_df[valuation_df["Case"] == "Bull"].iloc[0]

base_fair = safe_float(base_row["Fair Value"], np.nan)
base_mos = safe_float(base_row["MOS Price"], np.nan)
bear_fair = safe_float(bear_row["Fair Value"], np.nan)
bull_fair = safe_float(bull_row["Fair Value"], np.nan)
implied_growth = reverse_implied_growth(current_price, base_metric, years, exit_multiple, discount_rate)
score, notes = assumption_score(growth, discount_rate, exit_multiple, margin_of_safety, years, metric_type)
verdict_title, verdict_text = get_verdict(current_price, base_fair, base_mos, bear_fair, bull_fair)

upside = np.nan
if current_price > 0 and np.isfinite(base_fair):
    upside = (base_fair / current_price) - 1

# -------------------------
# Top metrics
# -------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Base Fair Value</div>
            <div class="metric-value">{money(base_fair)}</div>
            <div class="metric-help">Estimated value before margin of safety.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">MOS Price</div>
            <div class="metric-value">{money(base_mos)}</div>
            <div class="metric-help">Preferred entry price after safety buffer.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Upside/Downside</div>
            <div class="metric-value">{pct(upside)}</div>
            <div class="metric-help">Compared with current price entered.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Assumption Score</div>
            <div class="metric-value">{score}/100</div>
            <div class="metric-help">Checks if assumptions look realistic.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Verdict and charts
# -------------------------
left, right = st.columns([0.95, 1.35], gap="large")

with left:
    st.markdown(
        f"""
        <div class="verdict-box">
            <div class="verdict-title">{verdict_title}</div>
            <div class="verdict-text">{verdict_text}</div>
            <br>
            <span class="mini-badge">Implied Growth: {pct(implied_growth)}</span>
            <span class="mini-badge">MOS: {margin_of_safety*100:.0f}%</span>
            <span class="mini-badge">Horizon: {years}Y</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">🧠 What Warren would check next</div>
            <div class="section-subtitle">Valuation is only one part. A cheap weak business can still be expensive.</div>
        """,
        unsafe_allow_html=True,
    )
    checklist = [
        "Is debt low and manageable?",
        "Are ROE and ROCE consistently strong?",
        "Are profit margins stable or improving?",
        "Is CFO close to or higher than reported profit?",
        "Is free cash flow positive and durable?",
        "Does the company have pricing power or a moat?",
        "Is valuation comfortable after margin of safety?",
    ]
    for item in checklist:
        st.checkbox(item, value=False)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">📍 Valuation Map</div>
            <div class="section-subtitle">Compare current price with bear, base and bull valuation estimates.</div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(make_value_chart(company, current_price, valuation_df), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Case Table",
    "🔥 Sensitivity",
    "🍯 Assumption Notes",
    "📤 Share & Report",
    "📝 SEO Article Draft",
])

with tab1:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Bear / Base / Bull Scenario Table</div>
            <div class="section-subtitle">This table shows how valuation changes when growth, discount rate and exit multiple change.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_df = valuation_df.copy()
    for col in ["Growth", "Discount Rate"]:
        display_df[col] = display_df[col].map(lambda x: f"{x*100:.2f}%")
    display_df["Exit Multiple"] = display_df["Exit Multiple"].map(lambda x: f"{x:.2f}x")
    for col in ["Future Metric", "Fair Value", "MOS Price"]:
        display_df[col] = display_df[col].map(money)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Sensitivity Honeycomb</div>
            <div class="section-subtitle">Small changes in assumptions can create large changes in intrinsic value. This is why valuation should be used as a range, not a magic number.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        make_sensitivity_heatmap(base_metric, years, exit_multiple, margin_of_safety, growth, discount_rate),
        use_container_width=True,
        config=PLOTLY_MOBILE_CONFIG,
    )

with tab3:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Assumption Quality Notes</div>
            <div class="section-subtitle">This is the unique Financify layer. The tool does not only calculate value; it questions your assumptions.</div>
        """,
        unsafe_allow_html=True,
    )
    for n in notes:
        st.markdown(f"- {n}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning-box">
        <b>Important:</b> Intrinsic value is highly sensitive to future growth, exit multiple and discount rate. Use conservative assumptions and always check business quality before trusting any valuation output.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab4:
    report = build_report(
        company,
        metric_type,
        base_metric,
        current_price,
        years,
        growth,
        discount_rate,
        exit_multiple,
        margin_of_safety,
        display_df,
        verdict_title,
        verdict_text,
        implied_growth,
        score,
        notes,
    )

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Shareable Mini Report</div>
            <div class="section-subtitle">Use this as a hook: users can copy the report and share it with friends, bringing traffic back to your blog.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_area("Copy report", value=report, height=360)
    st.download_button(
        "⬇️ Download mini report",
        data=report,
        file_name=f"financify_intrinsic_value_{company.replace(' ', '_').lower() or 'stock'}.txt",
        mime="text/plain",
    )

    share_text = f"I estimated {company or 'a stock'} intrinsic value using Financify. Base fair value: {money(base_fair)}, MOS price: {money(base_mos)}. Try the free tool: {TOOLS_PAGE_URL}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(share_text)}"
    twitter_url = f"https://twitter.com/intent/tweet?text={quote_plus(share_text)}"
    st.markdown(f"[📲 Share on WhatsApp]({whatsapp_url})  &nbsp;&nbsp; [𝕏 Share on X]({twitter_url})", unsafe_allow_html=True)

with tab5:
    title, meta, excerpt, body = build_seo_draft(
        company,
        metric_type,
        base_metric,
        current_price,
        years,
        growth,
        discount_rate,
        exit_multiple,
        margin_of_safety,
        base_fair,
        base_mos,
    )
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">SEO Article Draft Generator</div>
            <div class="section-subtitle">This creates a human-editable WordPress draft around the tool result. Do not mass-publish blindly; add your own voice, data checks and final review.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("SEO title", value=title)
    st.text_area("Meta description", value=meta, height=90)
    st.text_area("Excerpt", value=excerpt, height=90)
    st.text_area("Article draft", value=body, height=520)

# -------------------------
# CTA + Disclaimer
# -------------------------
st.markdown(
    f"""
    <div class="cta-card">
        <h3>Want deeper business-quality analysis?</h3>
        <p>
        This free calculator estimates value. But serious investing also needs debt checks, margin trend, ROE, ROCE, CFO, FCF,
        valuation comfort and bubble-risk checks. That is where Financify Pro tools come in.
        </p>
        <p><b>Free users:</b> use simple tools for learning. <b>Pro users:</b> unlock deeper scans across Financify tools.</p>
        <p>👉 <a href="{SURECART_CHECKOUT_URL}" target="_blank" style="color:#111;font-weight:950;">Upgrade to Financify Pro</a> &nbsp; | &nbsp;
        <a href="{TOOLS_PAGE_URL}" target="_blank" style="color:#111;font-weight:950;">Explore all Financify tools</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="warning-box">
    <b>Educational disclaimer:</b> This tool is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. The estimates depend fully on user-entered assumptions. Please do your own research or consult a SEBI-registered investment adviser before making financial decisions.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer-note">🐝 Financify • Madness of Money Bees • Built for practical finance learners</div>
    """,
    unsafe_allow_html=True,
)
