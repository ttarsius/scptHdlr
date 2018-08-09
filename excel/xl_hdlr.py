#created at 2018-3-26
from xlrd import open_workbook,xldate_as_datetime
import xlwt
from xlutils.copy import copy

def find_lines_in_col(keywords,filename,colnum):
    workbook = open_workbook(filename)
    sheets = workbook.sheet_names()
    results = []

    for k in keywords:
        for s in sheets:
            sheet = workbook.sheet_by_name(s)
            nrow = sheet.nrows

            for i in range(0,nrow):
                if k in str(sheet.cell_value(i,colnum)):
                    row = sheet.row_values(i)
                    row.insert(0,s)
                    results.append(row)

    return results

#按关键字查找excel表，支持多关键字查找，返回命中行的列表（行首添加sheet名称）
def find_lines(keywords, filename):
    workbook = open_workbook(filename)
    sheets = workbook.sheet_names()
    results = []

    for k in keywords:
        for s in sheets:
            sheet = workbook.sheet_by_name(s)
            nrow = sheet.nrows
            ncol = sheet.ncols
            for i in range(0,nrow):
                for j in range(0,ncol):
                    #print(i," ",j," ",sheet.cell_value(i,j))
                    #if type(k) == type(sheet.cell_value(i,j)):
                    if k in str(sheet.cell_value(i,j)):
                        row = sheet.row_values(i)
                        for c in range(0,ncol):
                            if sheet.cell(i,c).ctype == 3:
                                row[c] = xldate_as_datetime(row[c],0).strftime("%Y/%d/%m %H:%M:%S")
                        #将sheet名头插到命中行
                        row.insert(0,s)
                        results.append(row)
                        break

    return results

#写入到新建的EXCEL文件
def write_lines(lines,filename,sheetname="sheet1"):
    workbook = xlwt.Workbook()
    sheet1   = workbook.add_sheet(sheetname,cell_overwrite_ok=True)

    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])):
            sheet1.write(i,j,lines[i][j])

    workbook.save(filename)

#写入到已有的EXCEL文件
def append_xlfiles(lines,filename,sheetname="sheet"):
    workbook = open_workbook(filename)
    sh_num = len(workbook.sheets())
    xl = copy(workbook)

    if sheetname == "sheet":
        sheetname = "sheet"+str(sh_num+1)

    sheet1 = xl.add_sheet(sheetname,cell_overwrite_ok=True)

    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])):
            sheet1.write(i,j,lines[i][j])

    xl.save(filename)

#
