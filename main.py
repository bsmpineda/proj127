from asyncio.windows_events import NULL
from email.policy import default
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(
    user = 'proj127', password='proj127', database = 'project127', host = 'localhost', port = '3306'
)

create_cursor = mariadb_connection.cursor(buffered = True, dictionary = True)
#the database return a dictionary

categCounter = 0

def categoryCount():
	global categCounter

	select_content = "SELECT category_id FROM category"
	create_cursor.execute(select_content)
	mycategories = create_cursor.fetchall()

	categCounter = len(mycategories) #get the length of mycategories


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
	print("[9] Add task to a category")
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

		printAll('category')

		category_id = input("\nEnter task category: ")

		if check_ID(category_id,'category'):
			insert_content = f"INSERT INTO task (title, details, deadline, status, category_id) VALUES ('{title}', '{details}', STR_TO_DATE('{deadline}', '%Y/%m/%d'), '{status}', {category_id})"
			create_cursor.execute(insert_content)
			mariadb_connection.commit()
			print("Succesfully created new Task!")
	else:
		print("Error: client must first create a category!")

def createCateg():
	global categCounter
	categoryCount()
	categCounter += 1
	categ_name = input("\nEnter category name (must not exceed 15 characters): ")
	categ_description = input("Enter category description (must not exceed 100 characters): ")
	insert_content = f"INSERT INTO category (name, description) VALUES ('{categ_name}', '{categ_description}')"
	create_cursor.execute(insert_content)
	mariadb_connection.commit()

	print("Succesfully created new Category!")

#select all from the 'table' then return a list of dictionary
def selectAll(table):
    select_query = 'SELECT * FROM {}'
    create_cursor.execute(select_query.format(table))

    selected_items = create_cursor.fetchall() #fetch all the matched tuples
    #selected_items is a DICTIONARY

    return selected_items

#print all either from task or category table
def printAll(table):
	selected_items = selectAll(table)
	print('\n')
	
	for x in selected_items:
		for key, value in x.items():
			print(str(key) + ": " +  str(value)) # key: value

		if table=='task':
			id = x["category_id"]
			create_cursor.execute(f"select name from category where category_id = '{id}'")
			categName = create_cursor.fetchone() #get the query
			name = categName["name"] #get the value
			print(f"Category name: {name}")
			
		print('\n')
		
def updateOneTask(col_name, newData, id):
    #UPDATE task SET <col_name> = <newData> WHERE task_id = <id> 
	update_query = "UPDATE task SET " + col_name + " = '"+ newData +"' WHERE task_id = " + str(id) 
	create_cursor.execute(update_query) 
	mariadb_connection.commit()
	print("Task's " + col_name + " with id #" + id + " is updated successfully!")
	

	
#check if id exist
def check_ID(id, table): 
	create_cursor.execute(f"select {table}_id from {table} where {table}_id = '{id}'")
	
	check_exist = create_cursor.fetchall()
	if check_exist:
		return True
	else:
		print("ID does not exist!")
		return False

def deleteTask(id):
	delete_query = "DELETE FROM task WHERE task_id =" + str(id)
	create_cursor.execute(delete_query)
	mariadb_connection.commit()
	print("Task is successfully deleted!")

def addTasktoCategory(task_id, categ_id):
	query = f"UPDATE task SET category_id = '{categ_id}' WHERE task_id = '{task_id}'"
	create_cursor.execute(query)
	mariadb_connection.commit()
	print("Task is successfully added to a category!")


print("\n----------------- Welcome!!! -----------------")
categoryCount()

while True:
	c = menu()

	if c == 0:
		print("\n---- Thank you for using the application! ----")
		break
	elif c==1:
		createTask()
	elif c == 2: #edit task
		task_id = input("\nEnter id: ") #ask id
		if check_ID(task_id, 'task'): #check if id exists
			taskTable = selectAll('task') #get task table
			ctr = 0
			print("what do you want to edit:")
			for key in taskTable[0]:
				if key != 'task_id' and key != 'status' and key != 'category_id':
					print(f"\t[{ctr}] {key}")
					ctr += 1
			choiceNum = int(input("\tChoice: "))
			if choiceNum == 0:
				newData = input("\nNew title (must not exceed 15 characters): ")
				colname = 'title'
			elif choiceNum == 1:
				newData = input("\nNew task details (must not exceed 50 characters): ")
				colname = 'details'
			elif choiceNum == 2:
				newData = input("\nNew deadline date (format: YYYY/MM/DD): ")
				colname = 'deadline'
			elif choiceNum == 2:
				newData = input("\nNew deadline date (format: YYYY/MM/DD): ")
				colname = 'deadline'
			# elif choiceNum == 3:
			# 	printAll('category')
			# 	newData = input("New category: ")
			# 	colname = 'category_id' 
			# 	if not(check_ID(newData, 'category')):
			# 		newData = None
							
			else:
				print("Invalid Choice!") 
				newData = None
			
			if newData is not None:
				updateOneTask(colname, newData, task_id)
			else:
				print("Unsuccessful edit\n")
	
	elif c == 3: #delete task
		task_id = input("\nEnter id: ")
		if check_ID(task_id, 'task'):
			deleteTask(task_id)
			
	elif c == 4: #view all task
		printAll('task')
		#kelangan din iprint ung categ_name
	elif c == 5: #update status into 'C'
		#printAll('task')
		task_id = input("\nEnter id: ") #ask id
		if check_ID(task_id, 'task'):
			complete = 'C'
			updateOneTask('status', complete, task_id)
	elif c == 6:
		createCateg()
		
	elif c == 8: #view all category
		printAll('category') #for all
		#dapat pala isa isa, ayusin ko na lang HAHAHA
		
	elif c == 9: #add task to a category
		task_id = input("\nEnter id: ")
		if check_ID(task_id, 'task'):
			categ_id = input("\nEnter category id: ")
			if check_ID(categ_id, 'category'):
				addTasktoCategory(task_id, categ_id)
		
	else:
		print("invalid input!")
