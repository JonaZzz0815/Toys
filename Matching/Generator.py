'''
Author: zhangqj
Date: 2021-06-05 23:28:52
LastEditTime: 2021-06-05 23:42:33
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Toys/Matching/Generator.py
'''
import functools
import xlrd
import xlwt
import random
def GenerateData(num_std,num_section):
    workbook =  xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('STD Prefer',cell_overwrite_ok=True)

    worksheet.write(0,0,label="index of Student")
    worksheet.write(0,1,label="Name")

    for i in range(num_section):
        worksheet.write(0,i+2,str(i)+" place")

    # worksheet.write(0,1,label="1st place")
    # worksheet.write(0,2,label="2nd place")
    # worksheet.write(0,3,label="3rd place")
    # worksheet.write(0,4,label="4th place")
    # worksheet.write(0,5,label="5th place")
    for i in range(0,num_std):
        worksheet.write(1+i,0,i)
        preference = [ j for j in range(num_section) ]
        random.shuffle(preference)
        for j in range(num_section):
            worksheet.write(1+i,2+j,preference[j])
    worksheet1 = workbook.add_sheet('SEC Prefer',cell_overwrite_ok=True)

    worksheet1.write(0,0,label="index of Section")
    worksheet1.write(0,1,label="Name")
    worksheet1.write(0,2,label="Capacity")
    for i in range(num_std):
        worksheet1.write(0,i+3,str(i)+" place")

    for i in range(0,num_section):
        worksheet1.write(1+i,0,i)
        preference = [ j for j in range(num_std) ]
        random.shuffle(preference)
        for j in range(num_std):
            worksheet1.write(1+i,3+j,preference[j])
    workbook.save("Source.xlsx")
    
if __name__=="__main__":
    GenerateData(5,2)