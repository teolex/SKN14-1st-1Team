import streamlit as st

import mysql.connector
from Car import Car

def __get_car_list(cursor):
	query = """
select distinct id,
       make,                                                                                    -- 제조사
       model,                                                                                   -- 모델명
       electric_motor,                                                                          -- 전기차/하이브리드 여부
       year,                                                                                    -- 연식
       vehicle_size_class,                                                                      -- 차량크기
       cylinders,                                                                               -- 실린더 수
       engine_displacement * 1000                               engine_displacement,            -- 배기량(cc)
       fuel_type1,                                                                              -- 주 연료
       fuel_type2,                                                                              -- 보조 연료
       time_to_charge_at_120v,                                                                  -- 충전시간(120v)
       time_to_charge_at_240v,                                                                  -- 충전시간(240v)
       epa_range_for_fuel_type2    * 1.60934                    epa_range_for_fuel_type2,       -- 완충 시 전기주행거리(km)
       combined_mpg_for_fuel_type1 * 1.60934 / 3.78541          combined_kpl_for_fuel_type1,    -- 주 연료 평균연비(km/l)
       combined_mpg_for_fuel_type2 * 1.60934 / 3.78541          combined_kpl_for_fuel_type2,    -- 보조 연료 평균연비(km/l)
       epa_fuel_economy_score,                                                                  -- 연비점수
       ghg_score,                                                                               -- 온실가스 점수
       transmission,                                                                            -- 변속기 종류
       transmission_descriptor,                                                                 -- 변속기 상세정보
       start_stop,                                                                              -- 아이들링 스탑 유무
       drive,                                                                                   -- 구동방식(FF,AWD,RWD)
       (2_door_luggage_volume + 4_door_luggage_volume) * 28.3   luggage_volume,                 -- 트렁크 용량(l)
       if(guzzler is null, 'GOOD', 'BAD')                       guzzler                         -- 연비 상태
from   menudb.all_vehicles_model_public info
order by make, year desc, model
"""
	cursor.execute(query)
	_tmp_cars = cursor.fetchall()
	cars_by_make = {}
	for tpl_car in _tmp_cars:
		car = Car(*tpl_car)
		lst = cars_by_make[car.make] if car.make in cars_by_make else []
		lst.append(car)
		cars_by_make[car.make] = lst

	#TODO make 별 리스트를 다시 한번 dict 로 mapping할지 말지 여부 결정 필요.
	#TODO 리스트를 어떤 기준으로 정렬할지 결정 필요.
	return cars_by_make

################################################################################
# @st.dialog("Choose a car to compare", width="large")
def show_cars():
	style = """
<style>
	a + em { display:block; color:gray; text-align:center; white-space:nowrap; text-overflow:ellipsis; overflow:hidden; }
	div[data-testid=stDialog] div[role=dialog] { width:80vw; }
	
	button[kind=tertiary] { width:100%; color:#afafaf; }
</style>
"""
	st.markdown(style, unsafe_allow_html=True)

	################################################################################

	if "mk" in st.query_params:
		if "mk" not in st.session_state:
			st.session_state["mk"] = []

		__make = st.query_params["mk"]
		st.session_state.mk.append(__make)

	################################################################################

	if "all_cars" not in st.session_state:
		config = {
			"host"		: "localhost",
			"port"		: 3306,			# 기본 포트 쓸 경우 생략가능
			"user"		: "skn14",
			"password"	: "skn14",
			"database"	: "menudb"
		}
		with mysql.connector.connect(**config) as conn:
			with conn.cursor() as cursor:
				make_cars_dict = __get_car_list(cursor)
				st.session_state["all_cars"] = make_cars_dict

		alphabet_group = {}
		for make in make_cars_dict:
			first_letter = make[0].upper()
			lst = alphabet_group[first_letter] if first_letter in alphabet_group else []
			lst.append(make)
			alphabet_group[first_letter] = lst

		alphabet_group = dict(sorted(alphabet_group.items()))
		st.session_state["alphabet_group"] = alphabet_group
	else:
		make_cars_dict = st.session_state["all_cars"]
		alphabet_group = st.session_state["alphabet_group"]

	################################################################################

	st.header("Choose cars to compare")

	col1, col2, col3 = st.columns([1,6,1])
	col1.write("Target :")
	col2.write(", ".join(st.session_state["mk"]) if "mk" in st.session_state else "")
	if col3.button("Clear", use_container_width=True):
		st.session_state["mk"] = []
		st.rerun()

	################################################################################

	COLUMN_CNT = 5
	tmp_logo = "https://qi-o.qoo10cdn.com/goods_image_big/7/1/5/3/7871437153_l.jpg"

	for letter,make_list in alphabet_group.items():
		car_names = ", ".join(make_list)
		car_names = car_names[:90] + "..." if len(car_names) > 90 else car_names

		label = rf"🚗 **{letter}** ({len(make_list)}) - _:gray[{car_names}]_"
		with st.expander(label):
			cols = st.columns(COLUMN_CNT)
			for i, make in enumerate(make_list):
				_idx = i % COLUMN_CNT
				with cols[_idx]:
					st.image(tmp_logo, use_container_width=True)
					# st.markdown(f"[![{make}]({tmp_logo})](link)*{make}*")
					# st.markdown(f"<a href='?mk={make}' target='_self'><img src='{tmp_logo}'></a>", unsafe_allow_html=True)
					if st.button(make, type="tertiary"):
						if "mk" not in st.session_state:
							st.session_state["mk"] = []
						st.session_state["mk"].append(make)
						st.rerun()

if __name__ == "__main__":
	show_cars()
