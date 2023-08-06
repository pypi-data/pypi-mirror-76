import xlrd
import xlwt

from xlutils.copy import copy

def copyCells(file,ncolumn_now,ncolumn_before,whichSheet,target_Sheet,old_row_start,old_row_end,new_row_start):# ncolumn_before表示以前表的数据，ncolmuns_now表示要覆盖的表的列,targetSheet2表示要写的文件表单
    workXlsx = xlrd.open_workbook(file, encoding_override="utf-8")# old_row_start表示旧表其实行，old_row_end表示旧表结束行，new_row_start表示新表起始行
    workSheet = workXlsx.sheet_by_index(whichSheet-1)  # 用地许可信息表
    old_row_start-=1

    new_row_start-=1
    print(old_row_end-old_row_start)

    for n in range(new_row_start, old_row_end-old_row_start+new_row_start):  # n表示现在的表中的数据行数
        for n2 in range(old_row_start,old_row_end ):  # n2表示要拷贝表的数据,旧表行
            if (n == n2 +new_row_start-old_row_start):
                print(workSheet.cell_value(n2, ncolumn_before-1))
                target_Sheet.write(n , ncolumn_now-1, workSheet.cell(n2, ncolumn_before-1).value)


