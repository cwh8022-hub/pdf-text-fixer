import streamlit as st
import pdfplumber
import requests
import json

st.set_page_config(page_title="PDF 文字修復工具", layout="centered")
st.title("🛡️ PDF 繁體中文文字修復")
st.write("這會提取 PDF 原始文字並重新排版至 Google 簡報，解決字體破碎問題。")

# 填入你剛才新建的文字版 GAS 網址
GAS_URL = "https://script.google.com/macros/s/AKfycbyQ5rPVpa3ryOSYaJAlFkyYEEreuasfegmKR0S3Wte0mrGyWjJlrSx1JbWxwyt6df0d2Q/exec"

uploaded_file = st.file_uploader("上傳 NotebookLM 產出的 PDF", type="pdf")

if uploaded_file and st.button("🚀 開始修復並存入 Google 簡報"):
    with st.spinner('正在分析文字編碼並重建排版...'):
        try:
            pages_content = []
            
            # 使用 pdfplumber 提取文字（這能避開 PDF 渲染時的字體破碎）
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # 簡單的清理：移除多餘空格，保留換行
                        pages_content.append(text)
            
            if not pages_content:
                st.error("無法從 PDF 中提取文字，請確認該 PDF 是否為掃描檔。")
            else:
                # 傳送至 GAS
                payload = {
                    "fileName": uploaded_file.name,
                    "content": pages_content
                }
                
                response = requests.post(GAS_URL, json=payload)
                
                if response.status_code == 200 and "docs.google.com" in response.text:
                    st.success("🎉 修復完成！已生成可編輯的繁體中文簡報。")
                    st.markdown(f"### [👉 點此開啟修復版簡報]({response.text})")
                else:
                    st.error(f"同步失敗，錯誤訊息: {response.text}")
                    
        except Exception as e:
            st.error(f"發生預期外錯誤: {str(e)}")

st.info("💡 小提醒：此模式適合純文字內容。若 PDF 含有大量圖表，建議使用原本的圖片版工具。")
