import streamlit as st

pages = {
    "차량 스펙 비교하기": [
        st.Page("app.py", title="한 눈에 비교하기"),
        st.Page("graph_page.py", title="그래프로 비교하기"),
    ]
}

pg = st.navigation(pages)
pg.run()