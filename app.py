import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import requests

st.title("🛡️ PDF 視覺 OCR 修復工具")
st.write("針對無法提取文字或字體破碎的 PDF，使用 OCR 進行強制辨識並重建簡報。")

GAS_URL = "https://script.google.com/macros/s/AKfycbyQ5rPVpa3ryOSYaJAlFkyYEEreuasfegmKR0S3Wte0mrGyWjJlrSx1JbWxwyt6df0d2Q/exec"

uploaded_file = st.file_uploader("上傳無法提取文字的 PDF", type="pdf")

if uploaded_file and st.button("🚀 啟動 OCR 辨識並存入雲端"):
    with st.spinner('正在進行 AI 視覺辨識 (OCR)... 這需要一點時間'):
        try:
            # 1. 將 PDF 轉為高清圖片
            images = convert_from_bytes(uploaded_file.read(), dpi=200)
            
            pages_content = []
            for img in images:
                # 2. 使用 Tesseract 辨識繁體中文 (chi_tra)
                # 提示：Streamlit Cloud 需要設定 packages.txt
                text = pytesseract.image_to_string(img, lang='chi_tra')
                if text:
                    pages_content.append(text)
            
            if not pages_content:
                st.error("OCR 辨識失敗，請確認 PDF 內容是否清晰。")
            else:
                # 3. 傳送至 GAS (沿用之前的文字版 GAS)
                payload = {"fileName": uploaded_file.name, "content": pages_content}
                response = requests.post(GAS_URL, json=payload)
                
                if response.status_code == 200:
                    st.success("🎉 OCR 修復完成！已生成繁體中文簡報。")
                    st.markdown(f"### [👉 點此開啟簡報]({response.text})")
        
        except Exception as e:
            st.error(f"錯誤: {str(e)}")
