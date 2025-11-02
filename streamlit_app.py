# 最初に google-generativeai がインストールされていない場合の対策
# Streamlitの「requirements.txt」に 'google-generativeai' を記載してください
# または、以下のようにPythonコード内で自動インストールすることもできます

import streamlit as st

# google-generativeaiが未インストールの場合、自動インストール
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

st.title("💬 Chatbot (Gemini API版)")
st.write(
    "このチャットボットはGoogle Gemini APIを使って応答を生成します。"
    "利用するにはGemini APIキーが必要です。[Gemini APIキーはこちら](https://aistudio.google.com/app/apikey)から取得可能です。"
    "事前に `pip install google-generativeai` を実行してください。"
)

# Gemini APIキー入力
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するにはGemini APIキーを入力してください。", icon="🗝️")
else:
    # Gemini API key設定
    genai.configure(api_key=gemini_api_key)

    # セッション状態でメッセージ保持
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # チャット履歴表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 入力フィールド
    if prompt := st.chat_input("どうぞご質問ください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini API履歴整形
        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            else:
                history.append({"role": "model", "parts": [m["content"]]})

        # Gemini chatモデル作成
        model = genai.GenerativeModel("gemini-2.5-pro")
        chat = model.start_chat(history=history[:-1])

        # Gemini APIで応答生成
        response = chat.send_message(prompt)
        answer = response.text

        # 応答表示
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
