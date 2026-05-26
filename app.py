import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="REAP 2026 Assistant", page_icon="🎓", layout="centered")

# Hide default Streamlit menus for a cleaner look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# 2. Load and Auto-Correct the FAQ Data
@st.cache_data
def load_faq_data():
    try:
        df = pd.read_excel('Updated_FAQ_REAP_2026.xlsx')

        # Auto-correct the .com to .co.in
        if 'FAQDescription' in df.columns:
            df['FAQDescription'] = df['FAQDescription'].str.replace('reaprajasthan.com', 'reaprajasthan.co.in')
            df['FAQDescription'] = df['FAQDescription'].str.replace('barchrajasthan.com', 'barchrajasthan.co.in')

        return df
    except Exception as e:
        st.error(f"Error loading FAQ file: {e}. Please ensure 'Updated_FAQ_REAP_2026.xlsx' is in the same folder.")
        return pd.DataFrame()


faq_df = load_faq_data()

# 3. Header & Clear Chat Button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🎓 REAP 2026 Assistant")
    st.caption("Ask me questions about REAP-2026 admissions.")
with col2:
    if st.button("🗑️ Clear", help="Restart the conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I help you with your REAP 2026 admission queries today?",
             "avatar": "🏛️"}
        ]
        st.rerun()

# 4. Quick Ask Buttons
st.write("**Frequently Asked Topics:**")
q_col1, q_col2, q_col3 = st.columns(3)
quick_prompt = None

if q_col1.button("📅 Registration Dates"):
    quick_prompt = "Registration Dates"
if q_col2.button("💰 Fee Details"):
    quick_prompt = "Fee Details"
if q_col3.button("📄 Domicile Rules"):
    quick_prompt = "do I need domicile certificate"

st.markdown("---")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you with your REAP 2026 admission queries today?",
         "avatar": "🏛️"}
    ]

# 6. Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# 7. Handle User Input
user_input = st.chat_input("Type your question here...")
prompt = quick_prompt or user_input

if prompt:
    # Show user message
    st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑‍🎓"})

    user_text = prompt.lower()
    bot_reply = "I couldn't find an exact answer for that. Please raise a complaint on the ticket helpline available in the candidate panel on the portal homepage and please save your ticket number for further communication."

    # Search logic
    if not faq_df.empty:
        for index, row in faq_df.iterrows():
            if pd.isna(row['FAQKeyWords']):
                continue

            keywords = [k.strip().lower() for k in str(row['FAQKeyWords']).split(',')]

            if any(word in user_text for word in keywords if word):
                bot_reply = str(row['FAQDescription'])
                break

                # Show bot response
    with st.chat_message("assistant", avatar="🏛️"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "avatar": "🏛️"})

# 8. Official Disclaimer
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** This virtual assistant provides answers based on the standard REAP-2026 FAQ. For official, binding information, please refer to the [REAP 2026 Information Booklet](https://www.reaprajasthan.co.in) or raise a ticket in your candidate panel.")