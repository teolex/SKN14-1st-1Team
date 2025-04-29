;####################################################################
;-- 테이블 복사하기
# create table all_vehicles_model_public_org like all_vehicles_model_public;          -- 테이블 구조 복사
# insert into all_vehicles_model_public_org select * from all_vehicles_model_public;  -- 테이블 데이터 복사

;-- 위 쿼리는, dump 를 import 해서 작업하는 경우 all_vehicles_model_public 가 원본인 상태에서
;-- 테이블을 all_vehicles_model_public_org 라는 이름으로 백업해놓기 위해 실행하는 쿼리임.

;-- dump 를 import 한 직후 delete_surplus.sql 을 수행한 적 있다면,
;-- 위 쿼리는 주석처리하고, 아래 쿼리를 수행해야 함.
drop table all_vehicles_model_public;
create table all_vehicles_model_public like all_vehicles_model_public_org;          -- 테이블 구조 복사
insert into all_vehicles_model_public select * from all_vehicles_model_public_org;  -- 테이블 데이터 복사

;####################################################################
;-- 안쓰는 컬럼 삭제
alter table all_vehicles_model_public drop column 2_door_passenger_volume;
alter table all_vehicles_model_public drop column 4_door_passenger_volume;
# alter table all_vehicles_model_public drop column annual_fuel_cost_for_fuel_type1;        -- UI 단에서 사용하는 컬럼으로, drop 대상에서 제외.
alter table all_vehicles_model_public drop column annual_fuel_cost_for_fuel_type2;
alter table all_vehicles_model_public drop column annual_petroleum_consumption_for_fuel_type1;
alter table all_vehicles_model_public drop column annual_petroleum_consumption_for_fuel_type2;
alter table all_vehicles_model_public drop column atv_type;
alter table all_vehicles_model_public drop column basemodel;
alter table all_vehicles_model_public drop column c240b_dscr;
alter table all_vehicles_model_public drop column c240dscr;
alter table all_vehicles_model_public drop column charge240b;
alter table all_vehicles_model_public drop column city_electricity_consumption;
alter table all_vehicles_model_public drop column city_gasoline_consumption;
alter table all_vehicles_model_public drop column city_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column city_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column co2_fuel_type1;
alter table all_vehicles_model_public drop column co2_fuel_type2;
alter table all_vehicles_model_public drop column co2_tailpipe_for_fuel_type1;
alter table all_vehicles_model_public drop column co2_tailpipe_for_fuel_type2;
alter table all_vehicles_model_public drop column combined_electricity_consumption;
alter table all_vehicles_model_public drop column combined_gasoline_consumption;
alter table all_vehicles_model_public drop column created_on;
alter table all_vehicles_model_public drop column engine_descriptor;
alter table all_vehicles_model_public drop column epa_city_utility_factor;
alter table all_vehicles_model_public drop column epa_combined_utility_factor;
alter table all_vehicles_model_public drop column epa_highway_utility_factor;
alter table all_vehicles_model_public drop column epa_model_type_index;
alter table all_vehicles_model_public drop column fuel_type;
alter table all_vehicles_model_public drop column ghg_score_alternative_fuel;
alter table all_vehicles_model_public drop column hatchback_luggage_volume;
alter table all_vehicles_model_public drop column hatchback_passenger_volume;
alter table all_vehicles_model_public drop column highway_electricity_consumption;
alter table all_vehicles_model_public drop column highway_gasoline_consumption;
alter table all_vehicles_model_public drop column highway_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column highway_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column mfr_code;
alter table all_vehicles_model_public drop column modified_on;
alter table all_vehicles_model_public drop column mpg_data;
alter table all_vehicles_model_public drop column phev_blended;
alter table all_vehicles_model_public drop column phev_city;
alter table all_vehicles_model_public drop column phev_combined;
alter table all_vehicles_model_public drop column phev_highway;
alter table all_vehicles_model_public drop column range_city_for_fuel_type1;
alter table all_vehicles_model_public drop column range_city_for_fuel_type2;
alter table all_vehicles_model_public drop column range_for_fuel_type1;
alter table all_vehicles_model_public drop column range_highway_for_fuel_type1;
alter table all_vehicles_model_public drop column range_highway_for_fuel_type2;
alter table all_vehicles_model_public drop column s_charger;
alter table all_vehicles_model_public drop column t_charger;
alter table all_vehicles_model_public drop column unadjusted_city_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column unadjusted_city_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column unadjusted_highway_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column unadjusted_highway_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column unrounded_city_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column unrounded_city_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column unrounded_combined_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column unrounded_combined_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column unrounded_highway_mpg_for_fuel_type1;
alter table all_vehicles_model_public drop column unrounded_highway_mpg_for_fuel_type2;
alter table all_vehicles_model_public drop column you_save_or_spend;

;####################################################################
;-- 2010 이전 데이터 삭제
delete from all_vehicles_model_public where year < 2010;