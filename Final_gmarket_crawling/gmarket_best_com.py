import requests
import openpyxl
from bs4 import BeautifulSoup

# 엑셀 파일에 쓰기 ( 랭킹, 상품명, 판매가격, 제품 상세 링크, 판매 업체 )
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.append(['랭킹', '상품명', '판매가격', '제품 상세 링크', '판매 업체'])
excel_sheet.column_dimensions['B'].width = 80
excel_sheet.column_dimensions['C'].width = 20
excel_sheet.column_dimensions['D'].width = 80
excel_sheet.column_dimensions['E'].width = 20


# 크롤링
URL = "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G06"

res = requests.get(URL)
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    cards = soup.select('.best-list')[1].select('ul > li')

    for index, card in enumerate(cards):
        title = card.select_one('.itemname')    # 상품명
        price = card.select_one('.s-price > strong')    # 판매 가격
        link = title['href']    # 제품 상세 링크

        res_info = requests.get(link)
        if res_info.status_code == 200:
            print(f'Running: {index + 1}')
            soup_info = BeautifulSoup(res_info.content, 'html.parser')
            provider_info = soup_info.select_one('.text__seller > a')   # 판매 업체

            excel_row = [index + 1, title.get_text(), price.get_text(),
                         link, provider_info.get_text()]
            excel_sheet.append(excel_row)
            # 엑셀 파일 D열에 링크를 하이퍼링크로 만든다
            excel_sheet.cell(row=index+2, column=4).hyperlink = link


cells = ['A1', 'B1', 'C1', 'D1', 'E1']
for cell_name in cells:
    cell = excel_sheet[cell_name]
    cell.alignment = openpyxl.styles.Alignment(horizontal='center')    # 가운데 정렬
    cell.font = openpyxl.styles.Font(color="01579B")    # 폰트 색깔 변경

excel_file.save("gmarket_best.xlsx")
excel_file.close()
print('Done!')
