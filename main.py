import streamlit	as st

from Key import Key

from model.Car import Car

################################################################################
def __print_style():
	style = """
	<style>
		div[data-testid=stMainBlockContainer] { max-width:unset; }
		div[data-testid=stColumn] { min-width:250px; max-width:250px; width:250px; }
		#root > div:nth-child(1) > div.withScreencast > div > div > section > div.stMainBlockContainer.block-container > div > div > div > div.stHorizontalBlock
		{ width:1000%; }
	</style>
"""

	st.markdown(style, unsafe_allow_html=True)

################################################################################
# 비교대상인 자동차 정보를 저장할 session_state 초기화
__key_comp_cars		= Key.key_comp_cars()
if __key_comp_cars not in st.session_state:
	st.session_state[__key_comp_cars] = []

cars = st.session_state[__key_comp_cars]

################################################################################
__print_style()
if st.button("Add a car to compare"):
	st.switch_page("pages/make_list.py")

################################################################################
len_cars = len(cars)
col_size = 1+len_cars if len_cars > 1 else [1,1,1]

if len_cars > 0:
	del_btn_cols = st.columns(col_size)
	for i,car in enumerate(cars):
		with del_btn_cols[i+1]:
			if st.button(f"{car.model}", icon=":material/delete:", use_container_width=True):
				st.session_state[__key_comp_cars].pop(i)
				st.rerun()

cols = st.columns(col_size, border=True)

################################################################################
FIRST_COLUMN = {
	"make"                           : "제조사",
	"model"                          : "모델명",
	"electric_motor"                 : "전기차/하이브리드 여부",
	"year"                           : "연식",
	"vehicle_size_class"             : "차량크기",
	"cylinders"                      : "실린더 수",
	"engine_displacement"            : "배기량(cc)",
	"fuel_type1"                     : "주 연료",
	"fuel_type2"                     : "보조 연료",
	"time_to_charge_at_120v"         : "충전시간(120v)",
	"time_to_charge_at_240v"         : "충전시간(240v)",
	"epa_range_for_fuel_type2"       : "완충 시 전기주행거리(km)",
	"combined_kpl_for_fuel_type1"    : "주 연료 평균연비(km/l)",
	"combined_kpl_for_fuel_type2"    : "보조 연료 평균연비(km/l)",
	"epa_fuel_economy_score"         : "연비점수",
	"ghg_score"                      : "온실가스 점수",
	"transmission"                   : "변속기 종류",
	"transmission_descriptor"        : "변속기 상세정보",
	"start_stop"                     : "아이들링 스탑 유무",
	"drive"                          : "구동방식(FF,AWD,RWD)",
	"luggage_volume"                 : "트렁크 용량(l)",
	"guzzler"                        : "연비 상태",
	"image"                          : ""
}
car_head = Car(None, **FIRST_COLUMN)
first_col = car_head.data_list()

with cols[0]:
	if len_cars:	st.image("1x1.png", use_container_width=True)
	else:			st.write("이미지")
	for val in first_col:
		st.write(val)

################################################################################
for i,car in enumerate(cars):
	with cols[i+1]:
		st.image(car.image)
		for val in car.data_list():
			st.write(val)
