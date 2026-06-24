import streamlit as st


def base_layout_home():
    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(135deg, #3b3fce 0%, #5865F2 40%, #8b5cf6 100%) !important;
            min-height: 100vh;
        }

        /* Let the page scroll if content genuinely doesn't fit (small screens / high zoom),
           but shrink spacing below so it fits on one screen at normal sizes. */
        [data-testid="stMain"] {
            overflow-y: auto !important;
        }

        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1rem !important;
            max-width: 900px !important;
        }

        /* Shrink the logo/title block on the home screen so cards aren't pushed below the fold */
        .stApp [data-testid="stImage"] img {
            max-height: 9vh !important;
            width: auto !important;
        }

        .stApp h1 {
            font-size: clamp(1.8rem, 4vh, 2.6rem) !important;
            margin: 0.4rem 0 !important;
        }

        .stApp::before {
            content: '';
            position: fixed;
            top: -150px;
            left: -150px;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(232,67,147,0.25) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }

        .stApp::after {
            content: '';
            position: fixed;
            bottom: -150px;
            right: -150px;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }

        .stApp div[data-testid="stColumn"] {
            background: rgba(255,255,255,0.12) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            border-radius: 2.5rem !important;
            padding: 1.5rem !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.3) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }

        .stApp div[data-testid="stColumn"] [data-testid="stImage"] img {
            max-height: 18vh !important;
            width: auto !important;
            margin: 0 auto !important;
        }

        .stApp div[data-testid="stColumn"]:hover {
            transform: translateY(-6px) !important;
            box-shadow: 0 20px 48px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        }

        .stApp div[data-testid="stColumn"] h2 {
            color: white !important;
            text-shadow: 0 2px 12px rgba(0,0,0,0.2) !important;
        }

        </style>
    """, unsafe_allow_html=True)


def base_layout_dashbord():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(160deg, #eef0ff 0%, #f5f3ff 50%, #fce7f3 100%) !important;
        }
        </style>
    """, unsafe_allow_html=True)


def base_layout():
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        /* ── Main container ── */
        .block-container {
            padding-top: 1.5rem !important;
            max-width: 780px !important;
        }
        
        
        /*hide the streamlit top water mark*/
        
        #MainMenu,footer,header{
            visibility:hidden;
        }

        /* ── Typography ── */
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2.6rem !important;
            line-height: 0.95 !important;
            margin-bottom: 0.2rem !important;
            color: #E84393 !important;
            letter-spacing: -0.5px !important;
            filter: drop-shadow(0 2px 8px rgba(232,67,147,0.3)) !important;
        }

        h2 {
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            color: #5865F2 !important;
        }

        h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            color: #1e293b !important;
        }

        p, label, li {
            font-family: 'Outfit', sans-serif !important;
        }

        /* ── Divider ── */
        hr {
            border: none !important;
            height: 2px !important;
            background: linear-gradient(90deg, #5865F2, #E84393) !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1.5rem !important;
            border-radius: 2px !important;
        }

        /* ── Text inputs ── */
        .stTextInput input {
            background: #ffffff !important;
            color: #1e293b !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 14px !important;
            padding: 14px !important;
            font-size: 17px !important;
            font-family: 'Outfit', sans-serif !important;
            transition: border 0.2s ease, box-shadow 0.2s ease !important;
        }

        .stTextInput input:focus {
            border: 2px solid #5865F2 !important;
            box-shadow: 0 0 0 4px rgba(88,101,242,0.1) !important;
        }

        .stTextInput input::placeholder {
            font-size: 16px !important;
            color: #94a3b8 !important;
        }

        [data-baseweb="input"] {
            border-radius: 14px !important;
            overflow: hidden !important;
            border: none !important;
        }

        /* ── Camera input button ── */
        [data-testid="stCameraInputButton"] {
            background: linear-gradient(135deg, #c9287a, #a81f63) !important;
            color: white !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            border-radius: 50px !important;
            border: none !important;
            padding: 10px 28px !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 15px rgba(169,31,99,0.35) !important;
        }

        [data-testid="stCameraInputButton"]:hover {
            filter: brightness(1.1) !important;
            box-shadow: 0 8px 24px rgba(169,31,99,0.5) !important;
            transform: translateY(-2px) !important;
        }

        /* ── Select box ── */
        .stSelectbox div[data-baseweb="select"] > div {
            background: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 14px !important;
            font-family: 'Outfit', sans-serif !important;
            min-height: 52px !important;
        }

        .stSelectbox div[data-baseweb="select"] > div,
        .stSelectbox div[data-baseweb="select"] > div * {
            color: #1e293b !important;
        }

        /* ── Text area ── */
        .stTextArea textarea {
            border-radius: 14px !important;
            background: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            font-family: 'Outfit', sans-serif !important;
        }

        /* ── Containers / cards ── */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff !important;
            border-radius: 20px !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 2px 12px rgba(88,101,242,0.07) !important;
            padding: 4px !important;
        }

        /* ── Dataframe / table ── */
        [data-testid="stDataFrame"] {
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 2px 12px rgba(88,101,242,0.07) !important;
        }

        /* Style the dataframe toolbar buttons */
        [data-testid="stDataFrameToolbar"] {
            background: white !important;
            border-radius: 12px !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 2px 8px rgba(88,101,242,0.1) !important;
            padding: 4px !important;
        }

        [data-testid="stDataFrameToolbar"] button {
            border-radius: 8px !important;
            color: #5865F2 !important;
            transition: background 0.2s ease !important;
        }

        [data-testid="stDataFrameToolbar"] button:hover {
            background: #eef0ff !important;
        }

        /* ── Alert / info boxes ── */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            font-family: 'Outfit', sans-serif !important;
            border: none !important;
        }

        /* ── Toast ── */
        [data-testid="stToast"] {
            border-radius: 16px !important;
            font-family: 'Outfit', sans-serif !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
        }

        /* ── Spinner ── */
        [data-testid="stSpinner"] p {
            font-family: 'Outfit', sans-serif !important;
            color: #5865F2 !important;
            font-weight: 600 !important;
        }

        /* ── File uploader ── */
        [data-testid="stFileUploader"] {
            border-radius: 16px !important;
        }

        /* ── Camera input ── */
        [data-testid="stCameraInput"] {
            border-radius: 16px !important;
            overflow: hidden !important;
        }

        /* ── Audio input — bigger mic icon ── */
        [data-testid="stAudioInput"] {
            border-radius: 14px !important;
        }

        [data-testid="stAudioInput"] button {
            min-width: 40px !important;
            min-height: 40px !important;
            width: 40px !important;
            height: 40px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #5865F2, #3b4ad4) !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(88,101,242,0.35) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stAudioInput"] button:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 8px 24px rgba(88,101,242,0.5) !important;
        }

        [data-testid="stAudioInput"] button svg {
            width: 18px !important;
            height: 18px !important;
            color: white !important;
            fill: white !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 5px !important; }
        ::-webkit-scrollbar-track { background: transparent !important; }
        ::-webkit-scrollbar-thumb {
            background: rgba(88,101,242,0.25) !important;
            border-radius: 10px !important;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(88,101,242,0.5) !important;
        }

        /* ══════════════════════════════════════
           BUTTONS
        ══════════════════════════════════════ */

        /* Hide the raw icon glyph that bleeds out of buttons, without collapsing text */
        .stButton > button [data-testid="stIconMaterial"] {
            display: none !important;
        }

        /* Base */
        .stButton > button {
            border-radius: 50px !important;
            border: none !important;
            min-height: 50px !important;
            padding: 10px 22px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: 0.3px !important;
            transition: all 0.2s ease !important;
            color: #ffffff !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
        }

        /* Force white text on ALL inner elements */
        .stButton > button *  {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-family: 'Outfit', sans-serif !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            filter: brightness(1.1) !important;
        }

        .stButton > button:active {
            transform: scale(0.98) !important;
        }

        /* Primary — deep pink */
        button[kind="primary"],
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #c9287a, #a81f63) !important;
            box-shadow: 0 4px 15px rgba(169,31,99,0.35) !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(169,31,99,0.5) !important;
        }

        /* Secondary — deep indigo */
        button[kind="secondary"],
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #3b4ad4, #2a35a8) !important;
            box-shadow: 0 4px 15px rgba(42,53,168,0.35) !important;
        }
        button[kind="secondary"]:hover {
            box-shadow: 0 8px 24px rgba(42,53,168,0.5) !important;
        }

        /* Tertiary — dark charcoal */
        button[kind="tertiary"],
        .stButton > button[kind="tertiary"] {
            background: linear-gradient(135deg, #1e1e2e, #2d2d44) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }
        button[kind="tertiary"]:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.35) !important;
        }

        </style>
    """, unsafe_allow_html=True)