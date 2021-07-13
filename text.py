from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 크롬 브라우저를 실행/조작하기 위한 드라이버 객체 생성
driver = webdriver.Chrome('./chromedriver')
# search = [["낚시가방",15],["낚시파라솔",15],["파라솔",15],["민물낚시대",10],["민물찌올림찌",10],["들어뽕낚시대",10],["민물낚시가방",10],["낚시가방 하드케이스",10],["올림찌",10],["루어낚시가방",10],["로드케이스",5],["루어가방",5],["낚시보조가방",5],["민물낚시용품",5],["바다낚시가방",5],["바다낚시찌",5],["올림찌",5],["루어낚시가방",5],["낚시받침대",3]]
searchTerm="가구"
search = [[searchTerm,1]]
# 키우라 , 테크만 , 다이나미스 , 아진통상 , 비블랙 , 부푸리
name=[]
price =[]
seller =[]
category2 =[]
rnp = []
register=[]
search1=[]
imageURL=[]
for x in range(len(search)):
    for i in range(search[x][1]):
        url = f"https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery={search[x][0]}&pagingIndex={i}&pagingSize=40&productSet=total&query={search[x][0]}&sort=rel&timestamp=&viewType=list"

        driver.get(url)
        body = driver.find_element_by_css_selector("body")
        for j in range(15):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.03)

        time.sleep(1.5)
        html = driver.page_source

        soup = BeautifulSoup(html,"html.parser")
        itemList = soup.find_all("li", attrs={"class" :"basicList_item__2XT81"})
        for item in itemList:
            search1.append(search[x][0])
            name.append(item.find("div", class_="basicList_title__3P9Q7").getText())
            price.append(item.select_one(".price_num__2WUXn").getText())
            seller.append(item.find("a", class_="basicList_mall__sbVax").get_text() if item.find("a", class_="basicList_mall__sbVax") is not None else "no seller")
            category2.append([c.get_text() for c in item.find_all("a",class_="basicList_category__wVevj")])
            rnp.append([e.get_text() for e in item.find_all("a", attrs={"class" : "basicList_etc__2uAYO"})])
            register.append(item.find("span", class_="basicList_etc__2uAYO").get_text() if item.find("span", class_="basicList_etc__2uAYO") is not None else "no register")
            imageURL.append(item.find("a", class_="thumbnail_thumb__3Agq6").find("img").get("src") if item.find("a", class_="thumbnail_thumb__3Agq6").find("img") is not None else "no image")

file =pd.DataFrame({
    "search1": search1,
    "seller" : seller,
    "register" :register,
    "name" : name,
    "price" : price,
    "category" : category2,
    "rnp" : rnp ,
    "imageURL" :imageURL
})

file.to_csv(f"{searchTerm}.csv", index=False)
