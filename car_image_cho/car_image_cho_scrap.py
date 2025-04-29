from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://auto.danawa.com/compare/?Codes=")

time.sleep(2)

# 추가하기 버튼 클릭
add_button = driver.find_element(By.XPATH, '//*[@id="Photo_1"]/div/button')
add_button.click()
time.sleep(2)

# 최종 수집 데이터 리스트
car_data = []

# ✅ 국산 브랜드 1~18
for idx in range(1, 17):
    try:
        # 국산 브랜드 클릭
        brand_xpath = f'//*[@id="layerPopup"]/div[2]/div[2]/div/div[1]/ul/li[{idx}]/a/span'
        brand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, brand_xpath))
        )
        brand_name = brand_button.text
        brand_button.click()
        time.sleep(2)

        # 차량 수집
        car_imgs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.img'))
        )

        for img in car_imgs:
            try:
                car_name = img.get_attribute("alt")
                img_url = img.get_attribute("src")
                car_data.append(("국산", brand_name, car_name, img_url))
            except Exception as e:
                print(f"모델 수집 오류: {e}")

        # 전체 브랜드로 나가기
        back_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layerPopup"]/div[2]/div[2]/div/div[1]/a/span'))
        )
        back_button.click()
        time.sleep(1)

    except Exception as e:
        print(f"국산 브랜드 인덱스 {idx} 처리 실패: {e}")
        continue

# ✅ 수입 브랜드 1~41
for idx in range(1, 42):
    try:
        # 수입 브랜드 클릭
        brand_xpath = f'//*[@id="layerPopup"]/div[2]/div[2]/div/div[2]/ul/li[{idx}]/a/span'
        brand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, brand_xpath))
        )
        brand_name = brand_button.text
        brand_button.click()
        time.sleep(2)

        # 차량 수집
        car_imgs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.img'))
        )

        for img in car_imgs:
            try:
                car_name = img.get_attribute("alt")
                img_url = img.get_attribute("src")
                car_data.append(("수입", brand_name, car_name, img_url))
            except Exception as e:
                print(f"모델 수집 오류: {e}")

        # 전체 브랜드로 나가기 (수입은 div[2])
        back_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layerPopup"]/div[2]/div[2]/div/div[1]/a/span'))
        )
        back_button.click()
        time.sleep(1)

    except Exception as e:
        print(f"수입 브랜드 인덱스 {idx} 처리 실패: {e}")
        continue

# ✅ 최종 저장
df = pd.DataFrame(car_data, columns=["구분", "브랜드", "차량명", "이미지 URL"])
df.to_csv("car_images_all_brands_final.csv", index=False, encoding="utf-8-sig")

driver.quit()