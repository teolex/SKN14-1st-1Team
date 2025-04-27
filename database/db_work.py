import streamlit as st

from Key import Key

import mysql.connector
from model.Car import Car

def __get_all_car_list(cursor) -> dict:
	"""
	DB 에서 전체 제조사의 전체 차종의 전체 스펙들을 조회하여 반환.\n
	반환값 예시)
\t		st.session_state["all_cars"] = {
\t\t		"Audi" : [],\n
\t\t		"Ford" : [
\t\t\t			Car( 'Car No.1', ... ),\n
\t\t\t			Car( 'Car No.2', ... ),\n
\t\t\t			...
\t\t		]
\t		}
	"""
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
	make_cars_dict = {}
	for tpl_car in cursor.fetchall():
		car = Car(*tpl_car)
		if car.make not in make_cars_dict:	make_cars_dict[car.make] = []
		make_cars_dict[car.make].append(car)

	#TODO make 별 리스트를 다시 한번 dict 로 mapping할지 말지 여부 결정 필요.
	#TODO 리스트를 어떤 기준으로 정렬할지 결정 필요.
	return make_cars_dict

################################################################################
def check_if_data_in_session() -> None:
	__key_all_cars		= Key.key_all_cars()
	__key_alpha_make	= Key.key_alpha_make()

	if __key_all_cars not in st.session_state:						# DB 조회한 정보가 세션에 없으면,
		config = {								# DB 접속정보 설정
			"host"		: "localhost",
			"port"		: 3306,
			"user"		: "skn14",
			"password"	: "skn14",
			"database"	: "menudb"
		}
		with mysql.connector.connect(**config) as conn:				# DB 에 접속해서
			with conn.cursor() as cursor:
				make_cars_dict = __get_all_car_list(cursor)			# 모든 차종 정보 조회하고
				st.session_state[__key_all_cars] = make_cars_dict	# session_state 에 저장.

		alphabet_group = {}
		for make in make_cars_dict:
			ch  = make[0].upper()									# 제조사 첫글자를 대문자로 따서,
			if ch not in alphabet_group:	alphabet_group[ch] = []
			alphabet_group[ch].append(make)							# 해당 알파벳의 list 에 제조사 추가.

		alphabet_group = dict(sorted(alphabet_group.items()))		# 알파벳 순서로 정렬하고,
		st.session_state[__key_alpha_make] = alphabet_group			# session_state 에 저장.
