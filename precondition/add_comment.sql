;# all_vehicles_model_public 테이블에 코멘트 추가
alter table all_vehicles_model_public comment '각 제조사별 차량 모델 정보';

;# brand_logos 테이블에 코멘트 추가
alter table brand_logos comment '각 제조사별 로고 이미지';


;# all_vehicles_model_public 테이블의 컬럼 코멘트 추가
alter table all_vehicles_model_public modify column id                           text comment '일련번호';
alter table all_vehicles_model_public modify column make                         text comment '제조사';
alter table all_vehicles_model_public modify column model                        text comment '모델명';
alter table all_vehicles_model_public modify column electric_motor               text comment '전기차/하이브리드 여부';
alter table all_vehicles_model_public modify column year                         text comment '연식';
alter table all_vehicles_model_public modify column vehicle_size_class           text comment '차량크기';
alter table all_vehicles_model_public modify column cylinders                    text comment '실린더 수';
alter table all_vehicles_model_public modify column engine_displacement          text comment '배기량(L)';
alter table all_vehicles_model_public modify column fuel_type1                   text comment '주 연료';
alter table all_vehicles_model_public modify column fuel_type2                   text comment '보조 연료';
alter table all_vehicles_model_public modify column time_to_charge_at_120v       text comment '충전시간(120v)';
alter table all_vehicles_model_public modify column time_to_charge_at_240v       text comment '충전시간(240v)';
alter table all_vehicles_model_public modify column epa_range_for_fuel_type2     text comment '완충 시 전기주행거리(mile)';
alter table all_vehicles_model_public modify column combined_mpg_for_fuel_type1  text comment '주 연료 평균연비(mile/gallon)';
alter table all_vehicles_model_public modify column combined_mpg_for_fuel_type2  text comment '보조 연료 평균연비(mile/gallon)';
alter table all_vehicles_model_public modify column epa_fuel_economy_score       text comment '연비점수';
alter table all_vehicles_model_public modify column ghg_score                    text comment '온실가스 점수';
alter table all_vehicles_model_public modify column transmission                 text comment '변속기 종류';
alter table all_vehicles_model_public modify column transmission_descriptor      text comment '변속기 상세정보';
alter table all_vehicles_model_public modify column start_stop                   text comment '아이들링 스탑 유무';
alter table all_vehicles_model_public modify column drive                        text comment '구동방식(FFAWDRWD)';
alter table all_vehicles_model_public modify column 2_door_luggage_volume        text comment '2 도어 트렁크 용량(L)';
alter table all_vehicles_model_public modify column 4_door_luggage_volume        text comment '4 도어 트렁크 용량(L)';
alter table all_vehicles_model_public modify column guzzler                      text comment '연비 상태';

;# brand_logos 테이블의 컬럼 코멘트 추가
alter table brand_logos modify column make      text comment '제조사';
alter table brand_logos modify column logo_url  text comment '로고 이미지 URL';