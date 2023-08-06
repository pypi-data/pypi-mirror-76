import xlrd

def getDataFromSpreadsheet(fileName, sheetname) :
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_name(sheetname)
    print(worksheet)
    rowEndIndex = worksheet.nrows - 1
    colEndIndex = worksheet.ncols - 1
    rowStartIndex = 1
    colStartIndex = 0
    testData = []
    dataRow = []

    curr_row = rowStartIndex
    while curr_row <= rowEndIndex:
         cur_col = colStartIndex
         while cur_col <= colEndIndex:
             cell_type = worksheet.cell_type(curr_row, cur_col)

             value = worksheet.cell_value(curr_row, cur_col)
             dataRow.append(value)
             cur_col+=1
         curr_row += 1
         testData.append(dataRow)
    return dataRow

def getTestCaseDataRow(testnme, excel_col, fileName, sheetname) :
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_name(sheetname)
    print(worksheet)
    rowEndIndex = worksheet.nrows - 1
    colEndIndex = worksheet.ncols - 1
    rowStartIndex = 1
    colStartIndex = 0
    testData = []
    dataRow = []
  
    print("Inputted TestName:", testnme)
    cur_row = 0
    excel_col = int(excel_col)
    Found = 0
    for i in range(rowEndIndex):  
        cur_row = cur_row+1  
        print("current row", cur_row)
        testvalue = worksheet.cell_value(cur_row, excel_col) 
        print(testnme, testvalue)        
        if testvalue == testnme: 
            Found = 1
            break
        
    if (Found == 0):
        return None
    	    	  
    print("after if break")                 
    cur_col = colStartIndex
    while cur_col <= colEndIndex:
         print(cur_col)
         cell_type = worksheet.cell_type(cur_row, cur_col)
         value = worksheet.cell_value(cur_row, cur_col)
         print(value)
         dataRow.append(value)
         cur_col+=1
         print(dataRow)               	     
    return dataRow

def getDataRowCount(fileName, sheetname) :
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_name(sheetname)
    print(worksheet)
    rowEndIndex = worksheet.nrows - 1   
    return rowEndIndex

def getDatabyRowIndex(excel_row, fileName, sheetname) :
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_name(sheetname)
    print(worksheet)
    colEndIndex = worksheet.ncols - 1
    colStartIndex = 0
    testData = []
    dataRow = []
    excel_row = int(excel_row)
    
    cur_col = colStartIndex
    while cur_col <= colEndIndex:
         print(cur_col)
         cell_type = worksheet.cell_type(excel_row, cur_col)
         value = worksheet.cell_value(excel_row, cur_col)
         print(value)
         dataRow.append(value)
         cur_col+=1
         print(dataRow)               	     
    return dataRow