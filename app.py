import streamlit as st
import pandas as pd

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
        df = pd.read_excel('Updated_FAQ_REAP_2026.xlsx')
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

# 4. Quick Ask Buttons
st.write("**Frequently Asked Topics:**")
q_col1, q_col2, q_col3 = st.columns(3)
quick_prompt = None

if q_col1.button("📅 Important Dates"): quick_prompt = "When will the application form be available?"
if q_col2.button("💰 Fee Details"): quick_prompt = "application fee"
if q_col3.button("📄 Domicile Rules"): quick_prompt = "do I need domicile certificate"

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
# This ensures 100% of the messages stay firmly inside the box!
chat_box = st.container(border=True)

with chat_box:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

# 8. Disclaimer
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This virtual assistant provides answers based on the standard REAP-2026 FAQ. For official, binding information, please refer to the [REAP 2026 Information Booklet](https://www.reaprajasthan.co.in) or raise a ticket in your candidate panel.")
