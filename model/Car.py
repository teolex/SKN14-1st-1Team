import re


class Car:

	def __init__(self,
				id,
				make,
				model,
				electric_motor,
				year,
				vehicle_size_class,
				cylinders,
				engine_displacement,
				fuel_type1,
				fuel_type2,
				time_to_charge_at_120v,
				time_to_charge_at_240v,
				epa_range_for_fuel_type2,
				combined_kpl_for_fuel_type1,
				combined_kpl_for_fuel_type2,
				epa_fuel_economy_score,
				ghg_score,
				transmission,
				transmission_descriptor,
				start_stop,
				drive,
				luggage_volume,
				guzzler,
				image=None):
		self.__id							= id
		self.__make							= make
		self.__model						= model
		self.__electric_motor				= electric_motor
		self.__year							= year
		self.__vehicle_size_class			= vehicle_size_class
		self.__cylinders					= cylinders
		self.__engine_displacement			= engine_displacement
		self.__fuel_type1					= fuel_type1
		self.__fuel_type2					= fuel_type2
		self.__time_to_charge_at_120v		= time_to_charge_at_120v
		self.__time_to_charge_at_240v		= time_to_charge_at_240v
		self.__epa_range_for_fuel_type2		= epa_range_for_fuel_type2
		self.__combined_kpl_for_fuel_type1	= combined_kpl_for_fuel_type1
		self.__combined_kpl_for_fuel_type2	= combined_kpl_for_fuel_type2
		self.__epa_fuel_economy_score		= epa_fuel_economy_score
		self.__ghg_score					= ghg_score
		self.__transmission					= transmission
		self.__transmission_descriptor		= transmission_descriptor
		self.__start_stop					= start_stop
		self.__drive						= drive
		self.__luggage_volume				= luggage_volume
		self.__guzzler						= guzzler
		self.__image						= image

	@property
	def make(self):							return self.__make
	@property
	def model(self):						return self.__model
	@property
	def electric_motor(self):				return self.__electric_motor
	@property
	def year(self):							return self.__year
	@property
	def vehicle_size_class(self):			return self.__vehicle_size_class
	@property
	def cylinders(self):					return self.__cylinders
	@property
	def engine_displacement(self):			return self.__engine_displacement
	@property
	def fuel_type1(self):					return self.__fuel_type1
	@property
	def fuel_type2(self):					return self.__fuel_type2
	@property
	def time_to_charge_at_120v(self):		return self.__time_to_charge_at_120v
	@property
	def time_to_charge_at_240v(self):		return self.__time_to_charge_at_240v
	@property
	def epa_range_for_fuel_type2(self):		return self.__epa_range_for_fuel_type2
	@property
	def combined_kpl_for_fuel_type1(self):	return self.__combined_kpl_for_fuel_type1
	@property
	def combined_kpl_for_fuel_type2(self):	return self.__combined_kpl_for_fuel_type2
	@property
	def transmission(self):					return self.__transmission
	@property
	def transmission_descriptor(self):		return self.__transmission_descriptor
	@property
	def start_stop(self):					return self.__start_stop
	@property
	def drive(self):						return self.__drive
	@property
	def guzzler(self):						return self.__guzzler
	@property
	def image(self):						return self.__image


	def data_list(self):
		return [
			self.__make,
			self.__model,
			self.__electric_motor,
			self.__year,
			self.__vehicle_size_class,
			self.__cylinders,
			self.__engine_displacement,
			self.__fuel_type1,
			self.__fuel_type2,
			self.__time_to_charge_at_120v,
			self.__time_to_charge_at_240v,
			self.__epa_range_for_fuel_type2,
			self.__combined_kpl_for_fuel_type1,
			self.__combined_kpl_for_fuel_type2,
			self.__epa_fuel_economy_score,
			self.__ghg_score,
			self.__transmission,
			self.__transmission_descriptor,
			self.__start_stop,
			self.__drive,
			self.__luggage_volume,
			self.__guzzler
		]

	#TODO 표현정보를 추가할 지 여부 확인.
	def __repr__(self): return f"Car ( {self.__make}, {self.__model}, {self.__year}, {self.__transmission} )"
