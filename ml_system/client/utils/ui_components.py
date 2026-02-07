import streamlit as st
from datetime import datetime

def display_header(title: str, subtitle: str = ""):
    """
    Consistent header style across pages.
    """
    st.markdown(f"""
        <h1 style='color: #064e3b; margin-bottom: 0;'>{title}</h1>
        <p style='color: #4b5563; font-size: 1.1rem; margin-top: 5px;'>{subtitle}</p>
        <hr style='border: 1px solid #d1fae5; margin: 20px 0;'>
    """, unsafe_allow_html=True)

def display_sidebar_info():
    """
    Sidebar information and status.
    """
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2382/2382461.png", width=60) 
        st.markdown("### Diabetes Risk AI")
        st.info("Ensure patient data is accurate before prediction.")
        
        st.divider()
        st.caption(f"Client v1.0.0")
        st.caption(f"Time: {datetime.now().strftime('%H:%M:%S')}")

def card_metric(label: str, value: str, delta: str = None, help: str = None):
    """
    Custom styled metric card.
    """
    st.metric(label=label, value=value, delta=delta, help=help)

def render_footer():
    """
    Standard footer.
    """
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            color: #6b7280;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.8rem;
            z-index: 1000;
        }
        </style>
        <div class="footer">
            © 2026 Healthcare AI Systems.<br>
            Not for direct diagnostic use without clinician review.<br>
            Made with ❤️ by <a href="https://linkedin.com/in/dr-gabriel-okundaye" target="_blank">Dr. Gabriel Okundaye</a>
        </div>
        """,
        unsafe_allow_html=True
    )
