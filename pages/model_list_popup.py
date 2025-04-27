import streamlit as st

from model.Car import Car
from database.db_work import *

################################################################################
def __print_style():
	style = """
	<style>
		div[data-testid=stDialog] div[role=dialog] { width:80vw; }

		button[kind=tertiary] { width:100%; color:#afafaf; }
	</style>
"""

	st.markdown(style, unsafe_allow_html=True)

@st.dialog("Choose models to compare", width="large")
def show_models(make:str=""):
	__print_style()
	check_if_data_in_session()

	make_cars_dict = st.session_state[Key.key_all_cars()]

	################################################################################
	st.header("자동차 선택")

	models = make_cars_dict[make]
	year_cars_dict = {}
	for car in models:
		if car.year not in year_cars_dict:
			year_cars_dict[car.year] = []
		year_cars_dict[car.year].append(car)
	year_cars_dict = dict(sorted(year_cars_dict.items(), reverse=True))

	COLUMN_CNT = 5
	for year,cars in year_cars_dict.items():
		with st.expander(f"{year}년식"):
			cols = st.columns(COLUMN_CNT)
			for i,car in enumerate(cars):
				idx = i % COLUMN_CNT
				with cols[	idx]:
					st.image(car.image, use_container_width=True)
					if st.button(f"{car.model} {car.fuel_type1}", type="tertiary", key=car.id_gen()):
						st.session_state[Key.key_comp_cars()].append(car)
						st.switch_page("main.py")
						# st.rerun()

if __name__ == "__main__":
	show_models("Ford")