import streamlit as st

from Key import Key

from model.Car import Car
from database.db_work import *
from pages.model_list_popup import *

################################################################################
def __print_style():
	style = """
	<style>
		div[data-testid=stMainBlockContainer] { width:90vw; max-width:unset; }

		button[kind=tertiary] { border:1px solid transparent; }
		button[kind=tertiary] p { width:100%; color:#afafaf; }
		
		button[kind=tertiary]:hover { border:1px solid red; }
		button[kind=tertiary]:hover p { color:red; }
	</style>
"""

	st.markdown(style, unsafe_allow_html=True)

################################################################################
def show_cars():
	__print_style()
	check_if_data_in_session()

	make_cars_dict = st.session_state[Key.key_all_cars()]
	alphabet_group = st.session_state[Key.key_alpha_make()]

	st.header("제조사 선택")
	st.markdown(f":gray[제조사 이름을 클릭하면 해당 제조사의 차량목록을 볼 수 있습니다.]")

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
					if st.button(make, type="tertiary", use_container_width=True):
						# if "mk" not in st.session_state:
						# 	st.session_state["mk"] = []
						# st.session_state["mk"].append(make)
						# st.rerun()
						show_models(make)

show_cars()