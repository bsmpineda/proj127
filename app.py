import mysql.connector as mariadb

myDB = mariadb.connect(user = 'proj127', password='proj127', database = 'project127', host = 'localhost', port = '3306')

cursor = myDB.cursor(buffered = True, dictionary = True)
#the database return a dictionary

def selectAll(table):

    select_query = 'SELECT * FROM {}'
    cursor.execute(select_query.format(table))

    selected_items = cursor.fetchall() #fetch all the matched tuples
    #selected_items is a DICTIONARY

    print('\n')

    for x in selected_items:
        for key, value in x.items():
           print(str(key) + ": " +  str(value)) # key: value
        print('\n')


#this update a task's status or details    
def updateOneTask(col_name, newData, id):
    #UPDATE task SET <col_name> = <newData> WHERE task_id = <id>
    update_query = "UPDATE task SET " + col_name + " = '"+ newData +"' WHERE task_id = " + str(id) 
    cursor.execute(update_query)



updateOneTask('status', 'C', 1)
selectAll('task')