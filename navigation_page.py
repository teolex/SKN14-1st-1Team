import streamlit as st

pages = {
    "Comp CarDiB": [
        st.Page("app.py", title="🚗 자동차 스펙 비교하기"),
        st.Page("graph_page.py", title="📊 자세하게 비교하기"),
    ]
}

pg = st.navigation(pages)
pg.run()