import json
import urllib.request
import re 
from bs4 import BeautifulSoup
from pprint import pprint

def MealData():

    # 급식이 담기는 공간 ( 비어있음 ) 일, 월, 화, 수, 목, 금, 토, 일,
    Pure_MealData = ['','','','','','','']

    # 학교 코드
    SchoolCode = "B100000599"

    # 급식이 나와있는 홈페이지
    URL = "https://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=" + SchoolCode + "&schulCrseScCode=4&schulKndScCode=4&schMmealScCode=2"

    # 홈페이지를 열고 읽어들인다.
    Open_URL = urllib.request.urlopen(URL,timeout=5).read()

    # BeautifulSoup를 사용해서 html 파일을 크롤링(긁어온다)
    Soup = BeautifulSoup(Open_URL, "html.parser")

    # 크롤링 데이터 중 급식 데이터만 추출
    Find_Contents = Soup.find(id="contents") # ID 값이 'contents'인 데이터만 추출
    Find_Table = Find_Contents.find_all("table") # table 이라는 태그를 가진 데이터를 가져온다
    Connect_Table = Find_Table[0] # 'Table'의 첫 번째 데이터를 가져온다
    Find_tr = Connect_Table.find_all("tr") # 'Table[0]'의 데이터 안에 있는 tr 태그를 가진 데이터를 추출 
    Connect_tr = Find_tr[2] # 'tr'의 두 번째
    Find_td = Connect_tr.find_all("td") # 'tr' 안에 있는 'td' 태그를 추출

    def Re_Data(Find_td):
        Data_List = str(Find_td) # Find_td 를 문자열로 변환
        Data_List = Data_List.replace('[', '').replace(']', '') # [, ] 를 빈 공간으로 치환
        Data_List = Data_List.replace('<br/>', '\n') # <br/> 을 \n 으로 치환
        Data_List = Data_List.replace('<td class="textC last">', '')
        Data_List = Data_List.replace('<td class="textC">', '')
        Data_List = Data_List.replace('</td>', '')
        Data_List = Data_List.replace('.', '').replace(',', '')
        Data_List = Data_List.replace('(h)', '')
        Data_List = re.sub(r"\d", "", Data_List)
        return str(Data_List)
 
    Pure_MealData[0] = Re_Data(Find_td[1])
    Pure_MealData[1] = Re_Data(Find_td[2])
    Pure_MealData[2] = Re_Data(Find_td[3])
    Pure_MealData[3] = Re_Data(Find_td[4])
    Pure_MealData[4] = Re_Data(Find_td[5])
    Pure_MealData[5] = "토요일은 굶는다"
    Pure_MealData[6] = "일요일도 굶는다"

    return Pure_MealData

Meal_List = MealData()

# 출력 예시
print("-월요일-\n" + Meal_List[0])
print("-화요일-\n" + Meal_List[1])
print("-수요일-\n" + Meal_List[2])
print("-목요일-\n" + Meal_List[3])
print("-금요일-\n" + Meal_List[4])
print("-토요일-\n" + Meal_List[5])
print("-일요일-\n" + Meal_List[6])