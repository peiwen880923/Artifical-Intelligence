'''
   有class版可用  --> movie_inf.py
'''
# 載入需要的套件
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

movie = input()

# 開啟瀏覽器視窗(Chrome)
driver = webdriver.Chrome()

# 前往電影網站
driver.get("https://play.google.com/store/movies?hl=zh_TW&gl=US")

driver.maximize_window() # For maximizing window
time.sleep(2)

# 取得搜尋按鈕
search_button = driver.find_element(By.CSS_SELECTOR,'button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc')
search_button.click()

# 輸入電影名稱
search = driver.find_element(By.CSS_SELECTOR,'input.HWAcU')
search.send_keys(movie)
search.send_keys(Keys.RETURN)

time.sleep(1)

driver.refresh()
time.sleep(1)

# 進入電影畫面
get_movie = driver.find_element(By.CSS_SELECTOR,'a.Si6A0c.ZD8Cqc')
url=get_movie.get_attribute('href')
driver.get(url)

# 取得電影資訊
get_text = driver.find_element(By.CLASS_NAME,'bARER')
print(get_text.text)

# # 取得電影類別
# get_category = driver.find_element(By.CSS_SELECTOR, 'WpHeLc.VfPpkd-mRLv6.VfPpkd-RLmnJb')
# print(get_category)

# 取得電影影片連結
get_video = driver.find_element(By.CSS_SELECTOR,'button.cvriud ')
link = get_video.get_attribute('data-trailer-url')
print(link)

# 點擊電影資訊按鈕
inf_button = driver.find_element(By.CSS_SELECTOR,'button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.QDwDD.mN1ivc.VxpoF')
inf_button.click()

time.sleep(1)

# 取得演員名單
get_actor = driver.find_element(by=By.XPATH, value="//*[@class='XCWUge']/div[2]/div[2]")
print(get_actor.text)

# 取得爛番茄評分
tomato_value=0
try:
   get_tomato = driver.find_element(by=By.XPATH, value="//*[@class='NWcwnb']/a")
   tomato_value = int(get_tomato.text[:-1])/100
   print(tomato_value)
except:
   tomato_value=0
   
# 關閉視窗
inf_button = driver.find_element(By.CSS_SELECTOR,'button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc.a8Z62d')
inf_button.click()


# 取得評論
try:
   get_commend_btn = driver.find_elements(By.CSS_SELECTOR,'button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.QDwDD.mN1ivc.VxpoF')
   get_commend_btn[1].click()
   get_commend_list = driver.find_elements(By.CLASS_NAME, 'h3YV2d')
   for i in range(len(get_commend_list)):
      print(get_commend_list[i].text)
except:
   print("no commend")

# 取得星級
star = 0
try:
   get_star = driver.find_element(By.CLASS_NAME, 'TT9eCd')
   star = float(get_star.text[0:3])
except:
   star = 0

time.sleep(2)

driver.quit()

