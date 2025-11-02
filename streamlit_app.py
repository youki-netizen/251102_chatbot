import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot (Gemini API版)")
st.write(
    "このチャットボットはGoogle Gemini APIを使って応答を生成します。"
    "利用するにはGemini APIキーが必要です。[Gemini APIキーはこちら](https://aistudio.google.com/app/apikey)から取得可能です。"
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するにはGemini APIキーを入力してください。", icon="🗝️")
else:
    # Set Gemini API key
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("どうぞご質問ください"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Geminiのリクエスト用に会話履歴を整形
        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            else:
                history.append({"role": "model", "parts": [m["content"]]})

        # Create Gemini chat model
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=history[:-1])  # 直近のユーザ入力はプロンプトとして渡す

        # Generate a response using the Gemini API
        response = chat.send_message(prompt)
        answer = response.text

        # Stream the response to the chat using `st.write_stream` (Gemini APIはストリーム不可なので直接表示)
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
