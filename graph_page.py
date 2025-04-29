import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.set_page_config(page_title="📊 자세하게 비교하기", layout="wide")

config = {
    "host": 'localhost',
    "port": 3306, # mysql
    "user": 'skn14',
    "password": 'skn14',
    "database": 'cardb'
}

# 캐싱을 적용한 데이터 로딩 함수
def load_data():
    try:
        with mysql.connector.connect(**config) as conn:
            # SQL 쿼리를 직접 실행하여 DataFrame으로 반환
            query = '''
                SELECT make AS Make,
                   model AS Model,
                   electric_motor AS Electric_Motor,
                   year AS Year,
                   vehicle_size_class AS Vehicle_Size_Class,
                   cylinders AS Cylinders,
                   (engine_displacement * 1000) AS Engine_Displacement,            -- 배기량(cc)
                   fuel_type1 AS Fuel_Type, 
                   fuel_type2 AS Fuel_Type2,
                   time_to_charge_at_120v AS Time_To_Charge_At_120v,
                   time_to_charge_at_240v AS Time_To_Charge_At_240v,
                   (epa_range_for_fuel_type2 * 1.60934) AS Epa_Range_For_Fuel_Type2,  -- 완충 시 전기주행거리(km)
                   (combined_mpg_for_fuel_type1 * 1.60934 / 3.78541) AS Combined_Kpl_For_Fuel_Type1,    -- 주 연료 평균연비(km/l)
                   (combined_mpg_for_fuel_type2 * 1.60934 / 3.78541) AS Combined_Kpl_For_Fuel_Type2,    -- 보조 연료 평균연비(km/l)
                   epa_fuel_economy_score AS Epa_Fuel_Economy_Score,
                   ghg_score AS GHG_Score,
                   transmission AS Transmission,
                   transmission_descriptor AS Transmission_Descriptor,
                   start_stop AS Start_Stop,
                   drive AS Drive,
                   ((2_door_luggage_volume + 4_door_luggage_volume) * 28.3) AS Luggage_Volume,
                   IF(guzzler IS NULL, 'GOOD', 'BAD') AS Guzzler_Score
                FROM cardb.all_vehicles_model_public
            '''
            # pd.read_sql()로 데이터 로드
            return pd.read_sql(query, conn)
    except mysql.connector.Error as err:
        print('DB 오류: ', err)
        # 에러 발생 시 빈 DataFrame 반환
        return pd.DataFrame()

df = load_data()

st.header("📊 자세하게 비교하기")

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
    if 'Fuel_Type' in df.columns:
        selected_fuel = st.selectbox('연료 종류(Fuel Type) 선택', ['전체'] + list(df['Fuel_Type'].unique()))
        if selected_fuel != '전체':
            filtered_df = filtered_df[filtered_df['Fuel_Type'] == selected_fuel]

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
        'Combined_Kpl_For_Fuel_Type1', 'Combined_Kpl_For_Fuel_Type2', 'Engine_Displacement',
        'Cylinders', 'Epa_Fuel_Economy_Score', 'GHG_Score', 'Luggage_Volume'
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
