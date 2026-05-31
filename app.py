import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="REAP-2026 Assistant", page_icon="🎓", layout="centered")

# Hide default menus, "Press Enter to apply" instruction, and apply custom REAP branding
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="InputInstructions"] { display: none !important; }
            [data-testid="stAppDeployButton"] { display: none !important; }
            .viewerBadge_container__ { display: none !important; }
            
            /* REAP BRANDING: Deep Maroon Headers */
            h1, h2, h3 { color: #A32626 !important; }
            
            /* REAP BRANDING: Maroon Buttons */
            div.stButton > button:first-child, div.stFormSubmitButton > button:first-child {
                background-color: #A32626 !important;
                color: white !important;
                border: none !important;
                font-weight: bold !important;
            }
            div.stButton > button:first-child:hover, div.stFormSubmitButton > button:first-child:hover {
                background-color: #8B1A1A !important; 
                transform: scale(1.02);
            }
            
            /* REAP BRANDING: Cream Bot Chat Bubbles */
            .stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) {
                background-color: #FDF5E6 !important;
                border: 1px solid #EEDcBa !important;
                border-radius: 10px;
            }
            
            /* REAP BRANDING: Maroon Metric Numbers */
            [data-testid="stMetricValue"] { color: #A32626 !important; }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Load Data (Cache Removed for Live Updates)
def load_faq_data():
    try:
        df = pd.read_excel('REAP_2026_FAQ.xlsx') 
        if 'FAQDescription' in df.columns:
            df['FAQDescription'] = df['FAQDescription'].str.replace('reaprajasthan.com', 'reaprajasthan.co.in')
            df['FAQDescription'] = df['FAQDescription'].str.replace('barchrajasthan.com', 'barchrajasthan.co.in')
        return df
    except Exception as e:
        st.error(f"Error loading FAQ file: {e}")
        return pd.DataFrame()

faq_df = load_faq_data()

# 3. Header, Clear Button & Disclaimer
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🎓 REAP-2026 Assistant")
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you with your REAP-2026 admission queries today?", "avatar": "🏛️"}]
        st.rerun()

st.caption("⚠️ **Disclaimer:** This virtual assistant provides answers based on the standard REAP-2026 FAQ. For official, binding information, please refer to the [REAP-2026 Website](https://www.reaprajasthan.co.in) or raise a ticket in your [candidate panel](https://help.reaprajasthan.co.in/FAQArea/FAQSupport/Index).")

# 4. VISUALIZATION DASHBOARD
st.write("") 
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric(label="REAP Status", value="Active 🟢", delta="2026 Session")
m_col2.metric(label="Total Colleges", value="73", delta="Govt. & Private")
m_col3.metric(label="Total Seats", value="27,627", delta="Across Rajasthan")
st.markdown("---")

with st.expander("📅 View Official Admission Timeline"):
    st.markdown("""
    **B.E. / B.Tech / B.Plan Course:**
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
    
    dist_data = pd.DataFrame({
        "District": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer", "Kota"],
        "Seats": [11781, 2291, 2040, 1568, 1414] 
    }).set_index("District")
    
    st.write("**Top 5 Hubs by Seat Availability:**")
    st.bar_chart(dist_data, color="#4da6ff")

# 5. Quick Ask Buttons
st.write("**Frequently Asked Topics:**")
q_col1, q_col2, q_col3 = st.columns(3)
quick_prompt = None

if q_col1.button("📅 Important Dates"): quick_prompt = "Registration Dates"
if q_col2.button("💰 Fee Details"): quick_prompt = "Fee Details"
if q_col3.button("📄 Domicile Rules"): quick_prompt = "Do I need domicile certificate?"

# 6. Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you with your REAP-2026 admission queries today?", "avatar": "🏛️"}
    ]

# 7. DRAW THE CHAT HISTORY FIRST (Dynamic Box)
chat_box = st.container(border=True)

with chat_box:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

# 8. DRAW THE INPUT FORM SECOND
prompt = quick_prompt
with st.form("chat_input_form", clear_on_submit=True, border=False):
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input("Ask a question:", placeholder="Type your question here...", label_visibility="collapsed")
    with btn_col:
        submitted = st.form_submit_button("Send 📩")

if submitted and user_input:
    prompt = user_input

# 9. SMART SEARCH PROCESS LOGIC & RERUN
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑‍🎓"})

    user_text = prompt.lower()
    user_words = user_text.split()
    bot_reply = "I couldn't find an exact answer for that. Please raise a complaint on the ticket helpline available in the candidate panel on the portal homepage and please save your ticket number for further communication."
    
    if not faq_df.empty:
        best_match_score = 0
        
        for index, row in faq_df.iterrows():
            if pd.isna(row['FAQKeyWords']):
                continue
                
            keywords = [k.strip().lower() for k in str(row['FAQKeyWords']).split(',')]
            score = 0
            
            for k in keywords:
                if not k: continue
                
                # Strong exact match
                if k in user_text:
                    score += len(k) * 2 
                    continue
                
                # Partial word match
                for u_word in user_words:
                    if len(u_word) >= 3 and (k.startswith(u_word) or u_word.startswith(k)):
                        score += len(k)
                        break 
            
            # Highest score wins
            if score > best_match_score:
                best_match_score = score
                bot_reply = str(row['FAQDescription'])

    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "avatar": "🏛️"})
    st.rerun()
