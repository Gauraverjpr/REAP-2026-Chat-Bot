import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="REAP 2026 Assistant", page_icon="🎓", layout="centered")

# Hide default menus
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Load Data
@st.cache_data
def load_faq_data():
    try:
        # POINT TO YOUR NEW EXCEL FILE HERE
        df = pd.read_excel('File_1_Final.xlsx')
        if 'FAQDescription' in df.columns:
            df['FAQDescription'] = df['FAQDescription'].str.replace('reaprajasthan.com', 'reaprajasthan.co.in')
            df['FAQDescription'] = df['FAQDescription'].str.replace('barchrajasthan.com', 'barchrajasthan.co.in')
        return df
    except Exception as e:
        st.error(f"Error loading FAQ file: {e}")
        return pd.DataFrame()

faq_df = load_faq_data()

# 3. Header & Clear Button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🎓 REAP 2026 Assistant")
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you with your REAP 2026 admission queries today?", "avatar": "🏛️"}]
        st.rerun()

# ----------------- NEW VISUALIZATION DASHBOARD -----------------
st.write("") # Adds spacing
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric(label="REAP Status", value="Active 🟢", delta="2026 Session")
m_col2.metric(label="Total Colleges", value="73", delta="Govt. & Private")
m_col3.metric(label="Total Seats", value="27,627", delta="Across Rajasthan")
st.markdown("---")

with st.expander("📅 View Official Admission Timeline"):
    st.markdown("""
    **B.E. / B.Tech Course:**
    * **13.05.2026:** Commencement of Online Registration
    * **10.06.2026:** Last Date for Fee Payment (Rs. 885/-)
    * **12.06.2026:** Last Date for Form Submission
    
    **B.Arch Course:**
    * **17.06.2026:** Commencement of Online Registration
    * **01.07.2026:** Last Date for Fee Payment (Rs. 885/-)
    * **03.07.2026:** Last Date for Form Submission
    """)

with st.expander("📊 View Seat Distribution Details"):
    st.write("**Total Capacity Breakdown:**")
    st.markdown("* **Private Institutions:** 20,091 Seats")
    st.markdown("* **Government Institutions:** 7,536 Seats")
    
# Verified data based on actual 27,627 seat matrix
    dist_data = pd.DataFrame({
        "District": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer", "Kota"],
        "Seats": [11781, 2291, 2040, 1568, 1414] 
    }).set_index("District")
    
    st.write("**Top 5 Hubs by Seat Availability:**")
    st.bar_chart(dist_data, color="#4da6ff")
# ---------------------------------------------------------------

# 4. Quick Ask Buttons
st.write("**Frequently Asked Topics:**")
q_col1, q_col2, q_col3 = st.columns(3)
quick_prompt = None

if q_col1.button("📅 Important Dates"): quick_prompt = "Registration Dates"
if q_col2.button("💰 Fee Details"): quick_prompt = "Fee Details"
if q_col3.button("📄 Domicile Rules"): quick_prompt = "Do I need domicile certificate?"

st.markdown("---")

# 5. Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you with your REAP 2026 admission queries today?", "avatar": "🏛️"}
    ]

# 6. GET INPUT & PROCESS LOGIC FIRST
user_input = st.chat_input("Type your question here...")
prompt = quick_prompt or user_input

if prompt:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑‍🎓"})

    # Search Logic
    user_text = prompt.lower()
    bot_reply = "I couldn't find an exact answer for that. Please raise a complaint on the ticket helpline available in the candidate panel on the portal homepage and please save your ticket number for further communication."

    if not faq_df.empty:
        for index, row in faq_df.iterrows():
            if pd.isna(row['FAQKeyWords']):
                continue
            keywords = [k.strip().lower() for k in str(row['FAQKeyWords']).split(',')]
            if any(word in user_text for word in keywords if word):
                bot_reply = str(row['FAQDescription'])
                break 

    # Append Bot Message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "avatar": "🏛️"})

# 7. DRAW THE BORDERED CHAT BOX SECOND
chat_box = st.container(border=True)

with chat_box:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

# 8. Disclaimer
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This virtual assistant provides answers based on the standard REAP-2026 FAQ. For official, binding information, please refer to the [REAP 2026 Information Booklet](https://www.reaprajasthan.co.in) or raise a ticket in your candidate panel.")

# 9. Force Scroll to Top
# This invisible iframe runs a quick JavaScript command to keep the view at the top
components.html(
    """
    <script>
        // Target the main scrollable container of the Streamlit app
        const mainContainer = window.parent.document.querySelector('.main');
        if (mainContainer) {
            // Smoothly scroll back to the top
            mainContainer.scrollTo({top: 0, behavior: 'smooth'});
        }
    </script>
    """,
    height=0 # Keeps it completely invisible
)



