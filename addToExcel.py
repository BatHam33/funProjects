import openpyxl as xl
realestatefile = xl.load_workbook('realEstateCostEval.xlsx')
sheet = realestatefile.get_sheet_by_name('Sheet1')
sheet['C5'] = purchaseprice
sheet['C6'] = downpaymentPercent
sheet['C7'] = interestRate
sheet['C8'] = lengthofmortgage
realestatefile.save(address+'_costEval.xlsx')