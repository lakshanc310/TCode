import psycopg2
import openpyxl

conn = psycopg2.connect(database = "UniHomes", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "admin",
                        port = 5432)

# Save Excel file location into a variable
excel_file = 'E:\\UW\\Triston_UK\\CityList.xlsx'

# Open the Excel workbook and load the active sheet into a variable
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# Create a list with the column names in the first row of the workbook
column_names = [column.value for column in sheet[1]]
print(column_names)
# Create an empty list 
data = []
# Iterate over the rows and append the data to the list
for row in sheet.iter_rows(min_row = 2, values_only = True): 
 data.append(row)

print(data)