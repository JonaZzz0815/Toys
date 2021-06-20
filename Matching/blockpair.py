"""
Created on Sat Jun 19 15:36:54 2021

@author: wangyancong
"""

import functools
import xlrd
import xlwt

book = xlrd.open_workbook("Source.xls")
sheet1 = book.sheets()[0]
sheet2 = book.sheets()[1]
num_stu = sheet1.nrows - 1  #学生人数
num_sec = sheet1.ncols - 2  #部门个数
blockpairs = 0

Studentpre = []
for i in range(num_stu):
    Studentpre.append(sheet1.row_values(i+1)[2:])# = sheet1.row_values(i+1)[2:]

Sectionpre = []
for i in range(num_sec):
    Sectionpre.append(sheet2.row_values(i+1)[3:])# = sheet1.row_values(i+1)[2:]
#############################################            
text = xlrd.open_workbook("MixedResult.xls")
SHEET = text.sheets()[0]

outcome = SHEET.col_values(2)[1:]
rank = SHEET.col_values(3)[1:]


for i in range(num_stu):
    if(int(rank[i]) != 0):
        for j in range(int(rank[i])):
            sec = int(Studentpre[i][j])
            if str(i) in Sectionpre[sec][:5]:
                blockpairs = blockpairs + 1







print(blockpairs)
