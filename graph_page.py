import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="자동차 스펙 비교", layout="wide")

EXCEL_FILE = 'all-vehicles-model.xlsx'

# 데이터 파일 존재 확인
if not os.path.exists(EXCEL_FILE):
    st.error(f"데이터 파일이 '{EXCEL_FILE}'로 존재하지 않습니다. 프로젝트 폴더에 파일을 넣어주세요.")
    st.stop()

# 캐싱을 적용한 데이터 로딩 함수
@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    return df

df = load_data()

st.title("🚗차량 스펙 비교하기🚗")
st.header("그래프로 비교하기")

# 컬럼명 확인 (앱 첫 화면에서만 보이게)
with st.expander("데이터 컬럼명 보기"):
    st.write(df.columns.tolist())

# 모델명 컬럼이 실제로 있는지 확인
if 'Model' not in df.columns:
    st.error("'Model' 컬럼이 데이터에 없습니다. 실제 모델명을 의미하는 컬럼명을 확인해 코드에서 수정하세요.")
    st.stop()

# 사이드바 필터
with st.sidebar:
    st.header("필터")
    filtered_df = df.copy()
    if 'Make' in df.columns:
        selected_make = st.selectbox('제조사(Make) 선택', ['전체'] + list(df['Make'].unique()))
        if selected_make != '전체':
            filtered_df = filtered_df[filtered_df['Make'] == selected_make]
    if 'Fuel Type' in df.columns:
        selected_fuel = st.selectbox('연료 종류(Fuel Type) 선택', ['전체'] + list(df['Fuel Type'].unique()))
        if selected_fuel != '전체':
            filtered_df = filtered_df[filtered_df['Fuel Type'] == selected_fuel]

# 비교할 모델 선택 (필터 적용)
selected_models = st.multiselect('비교할 모델을 선택하세요', filtered_df['Model'].unique())

if selected_models:
    compare_df = filtered_df[filtered_df['Model'].isin(selected_models)].copy()

    # Model+Year로 고유 식별자 생성 (중복 방지)
    if 'Year' in compare_df.columns:
        compare_df['Model_Year'] = compare_df['Model'].astype(str) + ' (' + compare_df['Year'].astype(str) + ')'
        x_col = 'Model_Year'
    else:
        x_col = 'Model'

    # 데이터 테이블 표시 (전치)
    transposed_df = compare_df.set_index(x_col).T
    # 중복 열 이름 처리
    transposed_df.columns = [
        f"{col}_{i}" if transposed_df.columns.duplicated()[i] else col
        for i, col in enumerate(transposed_df.columns)
    ]
    st.dataframe(transposed_df)

    # 비교할 스펙 컬럼 후보
    spec_cols = [
        'City Mpg For Fuel Type1', 'Highway Mpg For Fuel Type1', 'Combined Mpg For Fuel Type1',
        'Engine displacement', 'Cylinders', 'Co2 Fuel Type1', 'Annual Fuel Cost For Fuel Type1'
    ]
    # 실제 존재하는 컬럼만 사용
    spec_cols = [col for col in spec_cols if col in compare_df.columns]

    if spec_cols:
        selected_spec = st.selectbox('비교 항목을 선택하세요', spec_cols)
        fig = px.bar(compare_df, x=x_col, y=selected_spec, title=f'모델별 {selected_spec} 비교')
        st.plotly_chart(fig)
    else:
        st.info("비교 가능한 스펙(연비, 배기량 등) 컬럼이 없습니다.")
else:
    st.info("비교할 모델을 선택하세요.")
