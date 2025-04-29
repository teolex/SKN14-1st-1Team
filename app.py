import streamlit as st
import pandas as pd
import mysql.connector
# ✅ 1. 페이지 설정
st.set_page_config(page_title="🚗 자동차 스펙 비교하기", layout="wide")

### ✅ 0. 차량 이미지 매칭
car_images = {
    ("Hyundai", "Elantra", "2024"): 'Car_image/Hyundai_Elantra(2024).png',
    ("Kia", "Carnival", "2025"): "Car_image/Kia_Carnival(2025).png",
    ("Genesis", "G90 RWD", "2022"): "Car_image/Genesis_G90_RWD(2022).png",
}
default_image_url = "https://via.placeholder.com/300x200?text=No+Image"

config = {
    "host": 'localhost',
    "port": 3306, # mysql
    "user": 'skn14',
    "password": 'skn14',
    "database": 'cardb'
}

try:
    with mysql.connector.connect(**config) as conn:
        # SQL 쿼리를 직접 실행하여 DataFrame으로 반환
        query = '''
            select make,
                model,
                year,
                engine_displacement,
                fuel_type1 as fuel_type,
                transmission,
                combined_mpg_for_fuel_type1,
                annual_fuel_cost_for_fuel_type1
            FROM cardb.all_vehicles_model_public
        '''
        # pd.read_sql()로 데이터 로드
        df = pd.read_sql(query, conn)
except mysql.connector.Error as err:
    print('DB 오류: ', err)
    # 에러 발생 시 빈 DataFrame 반환
    df = pd.DataFrame()

# ✅ 3. 필요한 칼럼만 추출
useful_columns = [
    'make', 'model', 'year', 'engine_displacement',
    'fuel_type', 'transmission',
    'combined_mpg_for_fuel_type1', 'annual_fuel_cost_for_fuel_type1'
]
vehicle_df = df[useful_columns].dropna().reset_index(drop=True)

# ✅ 4. 칼럼 이름 정리
vehicle_df.rename(columns={
    'make': '브랜드',
    'model': '모델명',
    'year': '연식',
    'engine_displacement': '배기량 (L)',
    'fuel_type': '연료',
    'transmission': '변속기',
    'combined_mpg_for_fuel_type1': '복합연비 (mpg)',
    'annual_fuel_cost_for_fuel_type1': '연간 연료비 (USD)'
}, inplace=True)

try:
    with mysql.connector.connect(**config) as conn:
        # SQL 쿼리를 직접 실행하여 DataFrame으로 반환
        query = '''
            select make,
                logo_url
            FROM cardb.brand_logos
        '''
        # pd.read_sql()로 데이터 로드
        brand_logo_df = pd.read_sql(query, conn)
except mysql.connector.Error as err:
    print('DB 오류: ', err)
    # 에러 발생 시 빈 DataFrame 반환
    brand_logo_df = pd.DataFrame()

# ✅ 6. 브랜드명 -> 로고 URL 가져오는 함수
def get_brand_logo(brand):
    logo_row = brand_logo_df[brand_logo_df['make'] == brand]
    if not logo_row.empty:
        return logo_row['logo_url'].values[0]
    else:
        return "https://via.placeholder.com/150x50?text=No+Logo"

# ✅ 7. Streamlit 제목
st.markdown("<h1 style='text-align: center;'>🚗 자동차 스펙 비교하기</h1>", unsafe_allow_html=True)
st.markdown("---")

# ✅ 8. 3개 차량 선택
select_cols = st.columns(3)
selected_vehicles = []

for i in range(3):
    with select_cols[i]:
        # ✅ 브랜드 옵션 준비
        brand_options = ['--브랜드를 선택하세요--'] + sorted(vehicle_df['브랜드'].unique())

        # ✅ 기본 브랜드 설정
        default_brand = brand_options[0]
        selected_brand = st.session_state.get(f"brand_{i}", default_brand)

        # ✅ 제목 + 브랜드 로고 먼저
        title_cols = st.columns([3, 1])

        with title_cols[0]:
            st.markdown(f"### 🚘 차량 {i + 1} 선택")

        with title_cols[1]:
            # 브랜드를 선택했을 때만 로고를 표시
            if selected_brand != '--브랜드를 선택하세요--':
                brand_logo_url = get_brand_logo(selected_brand)
                if brand_logo_url == "https://via.placeholder.com/150x50?text=No+Logo":
                    st.markdown("""
                        <div style='
                            text-align: center;
                            font-size: 14px;
                            color: gray;
                            margin-bottom: 12px;
                        '>
                            로고가 없습니다
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f'<img src="{brand_logo_url}" width="80px" height="50px"/>', unsafe_allow_html=True)
                    # st.image(brand_logo_url)

        # ✅ 브랜드 선택
        selected_brand = st.selectbox(
            f"브랜드 선택 {i + 1}",
            brand_options,
            key=f"brand_{i}"
        )

        # ✅ 브랜드가 선택되었을 때만 모델명 선택
        if selected_brand != '--브랜드를 선택하세요--':
            model_options = ['--모델명을 선택하세요--'] + sorted(
                vehicle_df[vehicle_df['브랜드'] == selected_brand]['모델명'].unique()
            )
            selected_model = st.selectbox(
                f"모델명 선택 {i + 1}",
                model_options,
                key=f"model_{i}"
            )

            # ✅ 모델명이 선택되었을 때만 연식 선택
            if selected_model != '--모델명을 선택하세요--':
                year_options = ['--연식을 선택하세요--'] + list(
                    vehicle_df[
                        (vehicle_df['브랜드'] == selected_brand) &
                        (vehicle_df['모델명'] == selected_model)
                    ]['연식'].sort_values(ascending=False).unique()
                )
                selected_year = st.selectbox(
                    f"연식 선택 {i + 1}",
                    year_options,
                    key=f"year_{i}"
                )

                # ✅ 연식이 선택되었을 때만 차량 저장
                if selected_year != '--연식을 선택하세요--':
                    selected_vehicle = vehicle_df[
                        (vehicle_df['브랜드'] == selected_brand) &
                        (vehicle_df['모델명'] == selected_model) &
                        (vehicle_df['연식'] == selected_year)
                    ].iloc[0]
                    selected_vehicles.append(selected_vehicle)

# ✅ 9. 복합연비 최고 차량 찾기
best_fuel_efficiency_idx = -1
best_fuel_efficiency_value = -1

for idx, vehicle in enumerate(selected_vehicles):

    if int(vehicle['복합연비 (mpg)']) > best_fuel_efficiency_value:
        best_fuel_efficiency_value = int(vehicle['복합연비 (mpg)'])
        best_fuel_efficiency_idx = idx

# ✅ 선택한 차량 스펙 비교
st.markdown("---")
st.subheader("📊 선택한 차량 스펙 비교")

spec_cols = st.columns(3)
spec_list = ['브랜드', '모델명', '연식', '배기량 (L)', '연료', '변속기', '복합연비 (mpg)', '연간 연료비 (USD)']

### 🔥 팝업 상세보기 함수
@st.dialog("당신의 차는?")
def show_vehicle_detail(vehicle):
    st.dialog(f"🚘 {vehicle['브랜드']} {vehicle['모델명']} ({vehicle['연식']}) 상세 정보")
    # 이미지
    key = (vehicle['브랜드'], vehicle['모델명'], str(vehicle['연식']))
    image_path = car_images.get(key, default_image_url)

    if image_path:
        st.image(image_path)
    else:
        st.markdown("""
                <div style='
                    text-align: center;
                    font-size: 16px;
                    color: gray;
                    margin-bottom: 16px;
                '>
                    📷 사진이 없습니다
                </div>
            """, unsafe_allow_html=True)

    for spec in spec_list:
        st.markdown(f"""
            <div style='
                text-align: center;
                margin-bottom: 12px;
                font-size: 18px;
            '>
                <b>{spec}</b>: {vehicle[spec]}
            </div>
        """, unsafe_allow_html=True)


# 차량 출력 + 버튼 같이!
for i, col in enumerate(spec_cols):
    with col:
        if i < len(selected_vehicles):
            vehicle = selected_vehicles[i]

            # 이미지
            key = (vehicle['브랜드'], vehicle['모델명'], str(vehicle['연식']))
            image_url = car_images.get(key, default_image_url)

            if image_url == default_image_url:
                st.markdown("""
                                <div style='
                                    text-align: center;
                                    font-size: 16px;
                                    color: gray;
                                    margin-bottom: 16px;
                                '>
                                    📷 사진이 없습니다
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.image(image_url)


            # 차량명
            title = f"{vehicle['브랜드']} {vehicle['모델명']} ({vehicle['연식']})"
            if i == best_fuel_efficiency_idx:
                title += " ⭐️"
            st.markdown(f"<h3 style='text-align: center; margin-top: 20px; margin-bottom: 20px;'>{title}</h3>", unsafe_allow_html=True)

            # 스펙 출력
            for spec in spec_list:
                is_best = False

                if spec == '복합연비 (mpg)':
                    best_idx = max(range(len(selected_vehicles)), key=lambda idx: selected_vehicles[idx][spec])
                    is_best = (i == best_idx)
                elif spec == '연간 연료비 (USD)':
                    best_idx = min(range(len(selected_vehicles)), key=lambda idx: selected_vehicles[idx][spec])
                    is_best = (i == best_idx)

                st.markdown(f"""
            <div style='text-align: center; margin-bottom: 8px; font-size: 16px; {"background-color: #eaf4ef; border-radius: 5px; padding: 4px;" if is_best else ""}'>
            <b>{spec}</b>: {vehicle[spec]}
            </div>
                """, unsafe_allow_html=True)

            # 🔥 자세히 보기 버튼 (가운데 정렬)
            st.markdown("""
                <style>
                    button[kind=tertiary] p { border:1px solid gray; border-radius:5px; padding:5px 15px; }
                </style>
            """, unsafe_allow_html=True)

            if st.button(f"🚘 {vehicle['모델명']} 자세히 보기 🔍", key=f"detail_{i}", use_container_width=True, type="tertiary"):
                show_vehicle_detail(vehicle)


        else:
            st.markdown("🚗 차량을 선택하세요!", unsafe_allow_html=True)


# ✅ CSV 다운로드 버튼도 예외처리
if selected_vehicles:
    st.markdown("---")
    st.subheader("📥 비교 결과 다운로드")

    compare_result = pd.DataFrame(selected_vehicles)[spec_list]
    csv = compare_result.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="CSV 파일 다운로드",
        data=csv,
        file_name='차량_비교_결과.csv',
        mime='text/csv'
    )
else:
    st.warning("🚘 비교할 차량을 1개 이상 선택하세요!")