# pip install openpyxl
import openpyxl

from utils import do_crawling

# π important parameter. ν¬λ‘€λ§ ν  νμ΄μ§ μ§μ 
NUM_CRAWL_PAGE = 1

# π ν¬λ‘€λ§ μλ£λ μ λ³΄λ₯Ό μ μ₯ν  excel sheet_codi μ§μ 
wb_codi = openpyxl.Workbook()
sheet_codi = wb_codi.active
sheet_codi.append(["id",  "style", "img_url", "url", "popularity"])

wb_codi_tag = openpyxl.Workbook()
sheet_codi_tag = wb_codi_tag.active
sheet_codi_tag.append(["id", "tag"])

wb_item_codi_id = openpyxl.Workbook()
sheet_item_codi_id = wb_item_codi_id.active
sheet_item_codi_id.append(["id", "codi_id"])

workbooks = (wb_codi, wb_codi_tag, wb_item_codi_id)
sheets = (sheet_codi, sheet_codi_tag, sheet_item_codi_id)


# π μ§μ ν νμ΄μ§ μ λ§νΌ ν¬λ‘€λ§ μ§ννκΈ°
do_crawling(workbooks, sheets, NUM_CRAWL_PAGE)