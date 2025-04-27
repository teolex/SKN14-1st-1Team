import streamlit	as st

class Key:
	__key_all_cars		= "all_cars"
	__key_alpha_make	= "alphabet_group"
	__key_comp_cars		= "comp_cars_key"

	@staticmethod
	def key_all_cars():			return Key.__key_all_cars

	@staticmethod
	def key_alpha_make():		return Key.__key_alpha_make

	@staticmethod
	def key_comp_cars():		return Key.__key_comp_cars
