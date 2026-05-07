# =========================================================
# CUSTOM CSS
# =========================================================

def get_css(theme):
    return f"""
    <style>

    /* ================================
    MAIN APP
    ================================ */

    .stApp {{
        background-color: {theme['background']};
        color: white;
    }}

    /* ================================
    SIDEBAR
    ================================ */

    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #151722 0%,
            #11131D 100%
        );
        border-right: 1px solid {theme['primary']};
    }}

    /* ================================
    SIDEBAR NAV BUTTONS
    ================================ */

    section[data-testid="stSidebar"] button {{
        text-align: left !important;
        justify-content: flex-start !important;

        border-radius: 10px !important;

        margin-bottom: 8px !important;

        font-weight: 700 !important;

        background-color: transparent !important;

        color: #EAEAEA !important;

        border: 1px solid transparent !important;

        transition: all 0.15s ease-in-out !important;
    }}

    /* ACTIVE PAGE */

    section[data-testid="stSidebar"] button[kind="primary"] {{

        background-color: rgba(255,255,255,0.04) !important;

        color: #FFFFFF !important;

        border: 2px solid {theme['primary']} !important;

        box-shadow:
            0 0 12px rgba(255,255,255,0.08),
            0 0 6px {theme['secondary']} !important;
    }}

    /* HOVER EFFECT */

    section[data-testid="stSidebar"] button[kind="secondary"]:hover {{

        background-color: rgba(255,255,255,0.08) !important;

        color: {theme['primary']} !important;

        border: 1px solid {theme['primary']} !important;
    }}

    /* ================================
    SIDEBAR TEXT
    ================================ */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {{
        color: white !important;
    }}

    /* ================================
    SIDEBAR COLLAPSE ARROW
    ================================ */

    [data-testid="collapsedControl"] {{
        color: {theme['secondary']} !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    [data-testid="collapsedControl"] svg {{
        fill: {theme['secondary']} !important;
        color: {theme['secondary']} !important;
        opacity: 1 !important;
    }}

    /* ================================
    HEADINGS
    ================================ */

    h1, h2, h3 {{
        color: {theme['primary']};
    }}

    /* ================================
    METRIC CARDS
    ================================ */

    div[data-testid="metric-container"] {{

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.06),
                rgba(255,255,255,0.02)
            );

        border: 1px solid {theme['primary']};

        padding: 16px;

        border-radius: 14px;

        box-shadow:
            0 0 18px rgba(0,0,0,0.35);

        transition: 0.2s ease-in-out;
    }}

    div[data-testid="metric-container"]:hover {{

        transform: translateY(-2px);

        border: 1px solid {theme['secondary']};
    }}

    [data-testid="stMetricValue"] {{
        color: {theme['primary']};
    }}

    /* ================================
    SELECTBOXES / DROPDOWNS
    ================================ */

    div[data-baseweb="select"] > div {{

        background-color: #242633;

        border: 1px solid {theme['primary']};

        color: white;

        border-radius: 10px;
    }}

    div[data-baseweb="select"] svg {{
        fill: {theme['secondary']} !important;
        color: {theme['secondary']} !important;
        opacity: 1 !important;
    }}

    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg {{
        fill: {theme['secondary']} !important;
        color: {theme['secondary']} !important;
        opacity: 1 !important;
    }}

    /* ================================
    SLIDERS
    ================================ */

    .stSlider [data-baseweb="slider"] {{
        padding-top: 12px;
        padding-bottom: 12px;
    }}

    /* Full track glow layer */

    .stSlider [data-baseweb="slider"] > div > div {{
        background: linear-gradient(
            90deg,
            {theme['primary']} 0%,
            {theme['primary']} 45%,
            {theme['secondary']} 100%
        ) !important;

        height: 6px !important;
        border-radius: 999px !important;

        box-shadow:
            0 0 10px {theme['primary']},
            0 0 18px {theme['secondary']} !important;
    }}

    /* Force internal progress layers away from default red */

    .stSlider [data-baseweb="slider"] div {{
        border-color: {theme['primary']} !important;
    }}

    /* Slider knob */

    .stSlider [role="slider"] {{
        background-color: {theme['secondary']} !important;
        border: 2px solid {theme['primary']} !important;

        box-shadow:
            0 0 10px {theme['secondary']},
            0 0 18px {theme['primary']},
            0 0 24px rgba(255,255,255,0.20) !important;
    }}

    .stSlider [role="slider"]:hover {{
        transform: scale(1.08);

        box-shadow:
            0 0 14px {theme['secondary']},
            0 0 26px {theme['primary']},
            0 0 34px rgba(255,255,255,0.25) !important;
    }}

    /* Slider value labels */

    .stSlider [data-testid="stThumbValue"] {{
        color: {theme['primary']} !important;
        font-weight: 800 !important;
    }}

    .stSlider label {{
        color: white !important;
        font-weight: 600;
    }}

    .caption-spacer {{
        height: 38.5px;
    }}

    /* ================================
    TABLES
    ================================ */

    [data-testid="stDataFrame"] {{
        border: 1px solid {theme['primary']};
        border-radius: 12px;
        overflow: hidden;
    }}

    /* ================================
    DIVIDERS
    ================================ */

    hr {{
        border-color: {theme['primary']};
    }}

    /* ================================
    GENERAL BUTTONS
    ================================ */

    .stButton>button {{

        border-radius: 10px;

        font-weight: 700;

        border: 1px solid {theme['primary']};

        background-color: rgba(255,255,255,0.04);

        color: white;
    }}

    .stButton>button:hover {{

        border: 1px solid {theme['secondary']};

        color: {theme['primary']};
    }}

    [data-testid="stNumberInput"] input {{
        background-color: #242633 !important;
        color: white !important;
        border: 1px solid {theme['primary']} !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-weight: 700 !important;
    }}

    </style>
    """