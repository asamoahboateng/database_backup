import os
import json
import mysql.connector
from datetime import date
#import zipfile
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
#headers = [i[0] for i in mycursor.description]
#print(headers)

for x in myresult:
    
    data2 = []
    #print(x)
    file_name = './'+folder_name+'/'+x[0]+'.json'
    f= open(file_name,'w')
    
    reponse = "\n|>> Fetching Data from Table "
    print(reponse)
    print("|-->> Table \t: {}".format(x[0]))
    
    fetch_query = "select * from " + x[0]
    mycursor.execute(fetch_query)
    headers = [i[0] for i in mycursor.description]
    
    tableName = x[0]
    
    #headCount = 0
    myresult = mycursor.fetchall()
    print("|-->> Entities \t: {}".format(len(myresult)))
    
    headCount = 0
    for x in myresult:
        #print(x) 
    
        #print(len(headers))
        #print('--')
        data1 = {}
        for xx in range(len(headers)):
            #print(str(xx)+'<<--')
            data1[headers[xx]] = str(x[xx])
            #print(str(len(x))+'--')
            
        #print(headCount)
        headCount = headCount+1
        
        #print(data1)
        #data2[headCount] = []
        
        data2.append(data1)
    #print(data2)
    
    fileData = data2
    #fileData = {"type":"table","name":tableName,"database":dbName,"data": data2}
    
    with open(file_name,'w+') as outfile:
        json.dump(fileData, outfile)

#zipping folder
zipfoldername = folder_name+'_'+ today.strftime("%d_%m_%Y")
print('|>> Zipping Folder')
shutil.make_archive(zipfoldername, 'zip', './'+folder_name)

time.sleep(5)
print('|>> Deleting Folder')
shutil.rmtree('./'+folder_name, ignore_errors=True)

