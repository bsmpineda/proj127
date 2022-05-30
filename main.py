import mysql.connector as mariadb

mariadb_connection = mariadb.connect(
    user = 'proj127', password='proj127', database = 'project127', host = 'localhost', port = '3306'
)

create_cursor = mariadb_connection.cursor(buffered = True, dictionary = True)
#the database return a dictionary

categCounter = 0

def menu():
	print("\nOptions:")
	print("[1] Create task")
	print("[2] Edit task")
	print("[3] Delete task")
	print("[4] View all task")
	print("[5] Mark task as done")
	print("[6] Add category")
	print("[7] Delete category")
	print("[8] View category")
	print("[9] Add taks to a category")
	print("[0] Exit")
	choice = int(input("Choice: "))
	return choice


def createTask():
	global categCounter

	if categCounter > 0:
		title = input("\nEnter title of task (must not exceed 15 characters): ")
		details = input("Enter task detail (must not exceed 50 characters): ")
		deadline = input("Enter deadline date (format: YYYY/MM/DD): ")
		status = "INC"

		select_content = "SELECT * FROM category"
		create_cursor.execute(select_content)
		mycategories = create_cursor.fetchall()
		print("\nList of existing categories\n")
		print(mycategories)

		category_id = input("Enter task category: ")

		insert_content = f"INSERT INTO task (title, details, deadline, status, category_id) VALUES ('{title}', '{details}', STR_TO_DATE('{deadline}', '%Y/%m/%d'), '{status}', {category_id})"
		create_cursor.execute(insert_content)
		mariadb_connection.commit()
	else:
		print("Error: client must first create a category!")

def createCateg():
	global categCounter
	categCounter += 1
	categ_name = input("\nEnter category name (must not exceed 15 characters): ")
	categ_description = input("Enter category description (must not exceed 100 characters): ")
	insert_content = f"INSERT INTO category (name, description) VALUES ('{categ_name}', '{categ_description}')"
	create_cursor.execute(insert_content)
	mariadb_connection.commit()

#select all either from task or category table
def selectAll(table):

    select_query = 'SELECT * FROM {}'
    create_cursor.execute(select_query.format(table))

    selected_items = create_cursor.fetchall() #fetch all the matched tuples
    #selected_items is a DICTIONARY

    print('\n')

    for x in selected_items:
        for key, value in x.items():
           print(str(key) + ": " +  str(value)) # key: value
        print('\n')


#this update a task's status or details    
def updateOneTask(col_name, newData, id):
    create_cursor.execute(f"select task_id from task where task_id = '{id}'")
    check_exist = create_cursor.fetchall()
    if check_exist:
        #UPDATE task SET <col_name> = <newData> WHERE task_id = <id>
        update_query = "UPDATE task SET " + col_name + " = '"+ newData +"' WHERE task_id = " + str(id) 
        create_cursor.execute(update_query)
        print("Task with id " + id + " is edited successfully!")
    else:
        print("ID does not exist!")

	
#check if id exist
def check_ID(id): 
	create_cursor.execute(f"select task_id from task where task_id = '{id}'")
	
	check_exist = create_cursor.fetchall()
	if check_exist:
		return True
	else:
		print("ID does not exist!")
		return False




print("\n----------------- Welcome!!! -----------------")

while True:
	c = menu()

	if c == 0:
		print("\n---- Thank you for using the application! ----")
		break
	elif c==1:
		createTask()
	elif c == 2: #edit task
		task_id = input("\nEnter id: ") #ask id
		if check_ID(task_id): #check if id exists
			newDetail = input("New detail: ")
			updateOneTask('details', newDetail, task_id)
			
	elif c == 4: #view all task
		selectAll('task')
	elif c == 6:
		createCateg()
	else:
		print("invalid input!")
		# menu()
