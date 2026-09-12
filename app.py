import streamlit as st
import plotly.graph_objects as go
from src.inference import mock_inference

# Configure Page
st.set_page_config(
    page_title="EcoGrid-Cast | Probabilistic Dispatch",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Industrial CSS Injection
st.markdown("""
<style>
    /* Base background and text */
    .stApp {
        background-color: #0a0a0b;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headings */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        letter-spacing: -0.04em;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 0.9;
        background: linear-gradient(to bottom, #ffffff, #a1a1aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 800px;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    .system-identifier {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #d48e4d;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #111113;
        border: 1px solid #232328;
        padding: 1.5rem;
        border-radius: 4px;
        box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        background-color: #17171a;
        color: #94a3b8;
        padding: 0.2rem 0.4rem;
        border-radius: 2px;
        border: 1px solid #232328;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- UI: HERO SECTION -----------------
st.markdown('<div class="system-identifier">■ SYSTEM IDENTIFIER // DE-LU GRID</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">PROBABILISTIC<br>DISPATCH</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Conformal day-ahead wholesale electricity price calibration and renewable generation forecasting. Precise, calibrated, and rigorously bounded under extreme market volatility.</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0; border-top: 1px solid #232328; margin: 2rem 0;'>", unsafe_allow_html=True)

# ----------------- UI: METRIC BAR -----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Empirical Coverage</div>
        <div class="metric-value">91.2%<span class="metric-tag">TARGET: 90%</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Bidding Zone</div>
        <div class="metric-value">DE-LU<span class="metric-tag">GERMANY-LUXEMBOURG</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Model Latency</div>
        <div class="metric-value"><50 ms<span class="metric-tag">PYTHON NATIVE</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- MAIN LAYOUT -----------------
main_col, side_col = st.columns([7, 3])

with side_col:
    st.markdown("### SCENARIO SIMULATOR")
    
    wind_speed = st.slider(
        "WIND SPEED (m/s)",
        min_value=-10.0,
        max_value=10.0,
        value=0.0,
        step=0.5,
        format="%f m/s"
    )
    
    solar_rad = st.slider(
        "SOLAR RADIATION (W/m²)",
        min_value=-200.0,
        max_value=200.0,
        value=0.0,
        step=10.0,
        format="%f W/m²"
    )
    
    show_renewables = st.toggle("Show Renewable Generation (GW)", value=False)
    
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1rem; background-color: #111113; border: 1px solid #232328; border-radius: 4px;">
        <h4 style="font-size: 0.8rem; color: #d48e4d; font-family: 'Inter', sans-serif;">SYSTEM NOTES</h4>
        <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b;">Adjust the wind and solar sliders to perturb the base weather forecast. Increased renewables typically suppress median day-ahead prices and tighten conformal intervals due to grid merit-order effects.</p>
    </div>
    """, unsafe_allow_html=True)

# Fetch Data
response = mock_inference(bidding_zone="DE_LU", horizon=48, wind_delta=wind_speed, solar_delta=solar_rad)
data = response.points

timestamps = [p.timestamp for p in data]
medians = [p.median_price_eur for p in data]
lowers = [p.lower_bound_05_eur for p in data]
uppers = [p.upper_bound_95_eur for p in data]
renewables = [p.renewable_generation_mw / 1000.0 for p in data]

# ----------------- UI: FAN CHART -----------------
with main_col:
    st.markdown("### 48-HOUR PRICE FORECAST")
    
    fig = go.Figure()

    # Lower Bound
    fig.add_trace(go.Scatter(
        x=timestamps, y=lowers,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Upper Bound (Fill)
    fig.add_trace(go.Scatter(
        x=timestamps, y=uppers,
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(212, 142, 77, 0.15)',
        line=dict(width=0),
        name='90% Confidence Interval',
        hoverinfo='skip'
    ))

    # Median Line
    fig.add_trace(go.Scatter(
        x=timestamps, y=medians,
        mode='lines',
        line=dict(color='#d48e4d', width=3, shape='spline'),
        name='Median Price (q0.50)',
        hovertemplate='%{y:.1f} €/MWh<extra></extra>'
    ))

    if show_renewables:
        fig.add_trace(go.Scatter(
            x=timestamps, y=renewables,
            mode='lines',
            line=dict(color='#10b981', width=2, dash='dot'),
            name='Renewable Gen. (GW)',
            yaxis='y2',
            hovertemplate='%{y:.1f} GW<extra></extra>'
        ))

    layout = dict(
        height=500,
        margin=dict(t=10, r=show_renewables and 60 or 20, b=50, l=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(text='TIME (CET)', font=dict(family='Inter', color='#64748b', size=10)),
            gridcolor='#232328',
            tickfont=dict(family='JetBrains Mono', color='#94a3b8', size=11),
        ),
        yaxis=dict(
            title=dict(text='DAY-AHEAD PRICE (€/MWh)', font=dict(family='Inter', color='#64748b', size=10)),
            gridcolor='#232328',
            tickfont=dict(family='JetBrains Mono', color='#94a3b8', size=11),
        ),
        legend=dict(
            orientation='h',
            y=-0.25,
            x=0.5,
            xanchor='center',
            font=dict(family='Inter', size=11, color='#94a3b8'),
        ),
        hovermode='x unified',
    )

    if show_renewables:
        layout['yaxis2'] = dict(
            title=dict(text='RENEWABLE GENERATION (GW)', font=dict(family='Inter', color='#10b981', size=10)),
            overlaying='y',
            side='right',
            gridcolor='rgba(16, 185, 129, 0.05)',
            tickfont=dict(family='JetBrains Mono', color='#10b981', size=11),
            showgrid=False,
        )

    fig.update_layout(**layout)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
