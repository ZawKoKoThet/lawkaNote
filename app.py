import streamlit as st
import google.generativeai as genai
st.write(genai.__version__)
import tempfile
import os

st.set_page_config(page_title="Loka Note App", page_icon="🎤")
st.title("🎤 Loka Note (AI Meeting Assistant)")
st.markdown("အစည်းအဝေး အသံဖိုင်တင်ပေးရုံဖြင့် မြန်မာလို Auto မှတ်တမ်းနှင့် အနှစ်ချုပ် ထုတ်ပေးပါမည်။")

api_key = st.text_input("Google API Key ထည့်ပါ", type="password")
uploaded_file = st.file_uploader("အသံဖိုင် သို့မဟုတ် ဗီဒီယိုဖိုင် ရွေးပါ", type=['mp3', 'wav', 'm4a', 'mp4'])

if st.button("✨ မှတ်တမ်းထုတ်ပါ"):
    if not api_key:
        st.error("ကျေးဇူးပြု၍ Google API Key အရင်ထည့်ပါ။")
    elif not uploaded_file:
        st.error("အသံဖိုင် အရင်ရွေးချယ်ပေးပါ။")
    else:
        with st.spinner("AI မှ အသံဖိုင်ကို နားထောင်နေပါသည်... အသံဖိုင်ကြာချိန်ပေါ်မူတည်၍ အနည်းငယ် ကြာနိုင်ပါသည်..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-pro")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name
                
                audio_file = genai.upload_file(path=temp_path)
                
                prompt = """
                You are an expert AI Meeting Assistant. Listen to this audio and extract:
                ### ၁။ အစည်းအဝေး ခေါင်းစဉ် (Meeting Title)
                ### ၂။ အဓိက အနှစ်ချုပ် (Meeting Gist)
                ### ၃။ အစည်းအဝေး မှတ်တမ်း (Detailed Transcript)
                ### ၄။ ဆက်လက်လုပ်ဆောင်ရန် (Action Items)
                Respond ENTIRELY in Myanmar (Burmese) language using Markdown.
                """
                
                response = model.generate_content([prompt, audio_file])
                
                st.success("အောင်မြင်ပါသည်။")
                st.markdown(response.text)
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: {e}")
