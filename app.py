import os
import tempfile

import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Loka Note", page_icon="🎤")

st.title("🎤 Loka Note (AI Meeting Assistant)")
st.write("အစည်းအဝေး အသံဖိုင်တင်ပြီး မြန်မာလို မှတ်တမ်းထုတ်ပါ။")

# SDK Version
st.caption(f"Google Generative AI SDK: {genai.__version__}")

api_key = st.text_input(
    "Google AI Studio API Key",
    type="password",
    help="Google AI Studio မှာထုတ်ထားတဲ့ API Key ကိုထည့်ပါ။"
)

uploaded_file = st.file_uploader(
    "အသံဖိုင်ရွေးပါ",
    type=["mp3", "wav", "m4a", "mp4"]
)

if st.button("✨ မှတ်တမ်းထုတ်ပါ"):

    if not api_key:
        st.error("API Key ထည့်ပါ။")
        st.stop()

    if not uploaded_file:
        st.error("အသံဖိုင်ရွေးပါ။")
        st.stop()

    try:
        # Configure API
        genai.configure(api_key=api_key)

        # Test API Key
        try:
            list(genai.list_models())
        except Exception as e:
            st.error("API Key မမှန်ပါ။")
            st.exception(e)
            st.stop()

        model = genai.GenerativeModel("gemini-1.5-pro")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(uploaded_file.name)[1]
        ) as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        with st.spinner("အသံဖိုင် Upload လုပ်နေပါသည်..."):
            audio = genai.upload_file(temp_path)

        prompt = """
သင်သည် AI Meeting Assistant ဖြစ်သည်။

ဒီအသံဖိုင်ကို နားထောင်ပြီး

၁။ အစည်းအဝေးခေါင်းစဉ်
၂။ အဓိကအနှစ်ချုပ်
၃။ အသေးစိတ်မှတ်တမ်း
၄။ Action Items
၅။ တာဝန်ယူသူ (ရှိလျှင်)
၆။ ဆုံးဖြတ်ချက်များ

အားလုံးကို မြန်မာဘာသာဖြင့် Markdown Format ဖြင့် ထုတ်ပေးပါ။
"""

        with st.spinner("AI မှ အသံကို စစ်ဆေးနေပါသည်..."):

            response = model.generate_content(
                [prompt, audio],
                request_options={"timeout": 600},
            )

        st.success("ပြီးပါပြီ")

        st.markdown(response.text)

        try:
            os.remove(temp_path)
        except:
            pass

    except Exception as e:
        st.error("Error ဖြစ်နေပါသည်")
        st.exception(e)