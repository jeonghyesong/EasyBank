#kb캐피탈 금융용어 크롤링


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# 1. WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# 2. 사이트 열기
url = "https://m.kbcapital.co.kr/cstmrPtct/fnncInfoSqre/fnncTmng.kbc"
driver.get(url)

total_pages = 17

terms = set()

# “다음 그룹” 버튼 한 번만 누르기 위한 플래그
next_group_clicked = False

for page in range(1, total_pages + 1):
    # 1~10 페이지: 그냥 숫자 버튼 클릭
    if 1 < page <= 10:
        btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(page))))
        btn.click()

    # 11~17 페이지: 아직 한 번도 그룹 전환을 안 했다면 '>' 버튼 클릭
    elif page > 10 and not next_group_clicked:
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next")))
        next_btn.click()
        next_group_clicked = True
        # 11번 페이지는 next_btn 클릭으로 이미 이동됨 → 건너뛰고 크롤링만
    # 11~17 중 12~17: 숫자 버튼 클릭
    elif page > 10 and next_group_clicked:
        btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(page))))
        btn.click()

    # 페이지 전환 대기: “li.on a” 텍스트가 현재 page 숫자일 때까지
    wait.until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, "ul.pagi-num li.on a"),
        str(page)
    ))

    # 용어 요소 충분히 로드될 때까지 대기 (마지막 페이지만 1~9개, 나머진 10개)
    expected_min = page == total_pages and 1 or 10
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "span.tit")) >= expected_min)

    # 실제 크롤링
    for elem in driver.find_elements(By.CSS_SELECTOR, "span.tit"):
        terms.add(elem.text.strip())

    print(f"{page}페이지 크롤링 완료 (총 {len(terms)}개)")

    # 약간 쉬었다가 다음 페이지로
    time.sleep(0.2)

# 결과 CSV 저장
with open("kb_financial_terms.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["금융용어"])
    for term in sorted(terms):
        writer.writerow([term])

driver.quit()
