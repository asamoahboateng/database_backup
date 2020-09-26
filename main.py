import os
import json
import mysql.connector
from datetime import date
import shutil
import time

#today
today = date.today()

#folder name
folder_name = 'place_folder_name'

#make folder
if not os.path.exists('./'+folder_name):
    os.makedirs('./'+folder_name)
    
#connection to database
dbHost = "server ip"
dbUser = "database username"
dbPass = "database password"
dbName = "database name"

dbHost = "127.0.0.1"
dbUser = "root"
dbPass = ""
dbName = "esoft"

mydb = mysql.connector.connect(
  host=dbHost,
  user=dbUser,
  password=dbPass,
  database=dbName
)

#create cursor
mycursor = mydb.cursor()

#query
mycursor.execute("show tables")

myresult = mycursor.fetchall()

for (x,) in myresult: #tuple unpacking
    
    data2 = []
    file_name = './'+folder_name+'/'+x+'.json'
    
    #reponse = "\n|>> Fetching Data from Table "
    print("\n|>> Fetching Data from Table ")
    print("|-->> Table \t: {}".format(x))
    
    fetch_query = "select * from " + x
    mycursor.execute(fetch_query)
    
    headers = [i[0] for i in mycursor.description] #get column headers
    
   
    myresult = mycursor.fetchall() #all records
    print("|-->> Entities \t: {}".format(len(myresult)))
    
    for x in myresult:

        data1 = {}
        for xx in range(len(headers)):
            data1[headers[xx]] = str(x[xx])
            
        data2.append(data1)

    
    fileData = data2
    
    with open(file_name,'w+') as outfile:
        json.dump(fileData, outfile, sort_keys=True, indent=4)
    

#zipping folder
zipfoldername = folder_name+'_'+ today.strftime("%d_%m_%Y")
print('|>> Zipping Folder')
shutil.make_archive(zipfoldername, 'zip', './'+folder_name)


#time.sleep(5)
print('|>> Deleting Folder')
shutil.rmtree('./'+folder_name, ignore_errors=True)

