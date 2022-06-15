import streamlit as st
from util import call_text2img, translate_text

st.title("A text2img web application.")

st.markdown("""
使い方:
- 生成したい画像を表現する日本語の文章を入力して enter
- `英語に翻訳` ボタンを押して英語に翻訳する
- 必要があれば自分で英語の表現を手直しして enter
- （翻訳を使わずに最初から自分で英語の文章だけ入力してもよい）
- `画像を生成` ボタンを押して画像を生成する
""")

if "source_text" not in st.session_state:
    st.session_state["source_text"] = ""
if "target_text" not in st.session_state:
    st.session_state["target_text"] = ""

st.session_state["source_text"] = st.text_input("翻訳する日本語の文章", st.session_state["source_text"])

if st.button('英語に翻訳'):
    st.session_state["target_text"] = translate_text("EN", st.session_state["source_text"])
    st.session_state["target_text"] = st.text_input("if true: 翻訳された英語の文章", st.session_state["target_text"])
else:
    st.session_state["target_text"] = st.text_input("if false: 翻訳された英語の文章", st.session_state["target_text"])

if st.button("画像を生成"):
    st.write("工事中: clicked " + st.session_state["target_text"])
    st.image(call_text2img(st.session_state["target_text"]), caption="生成画像", clamp=True)
else:
    st.write("工事中: not clicked " + st.session_state["target_text"])
