
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = input('Enter the Url :')
#To be optimized by the title
tableNum = input('Enter the table number in sequence of the url :')


class parseTable:
    def parse_url(self,url,number):
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find_all('table')
        return self.parse_html_table(table[number])

    def parse_html_table(self,table):
        nRows = 0
        nColumns = 0
        columnsNames = []
        #Get the title of the table


        for rows in table.find_all('tr'):
            #Row Values
            rValues= rows.find_all('td')
            if(len(rValues)>0):
            #Number of rows with text, without being a Header
                nRows += 1
                if(nColumns ==0):
                    #Defining the number of columns
                    nColumns = len(rValues)
            titles = rows.find_all('th')

            # If there is already titles it don't add
            if(len(columnsNames)==0 and len(titles)>0):
                for title in titles:
                    columnsNames.append(title.get_text())
            columns = columnsNames if len(columnsNames) >0 else range(0,nColumns)
            df = pd.DataFrame(columns = columns, index=range(0,nRows))

        #Read about pandas to use the same loop
        #1 - Error for some reason if a use both I get a Bug
        rowMarker = 0
        for row in table.find_all('tr'):
            columnMarker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[rowMarker, columnMarker] = column.get_text()
                columnMarker += 1
            if len(columns) > 0:
                rowMarker += 1

        return df

hp = parseTable()
table = hp.parse_url(url,int(tableNum))
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
table.to_excel(writer,sheet_name='Sheet1')
print(table)
writer.save()
writer.close()
