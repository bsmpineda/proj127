import mysql.connector as mariadb

# connects the python code to the mysql database
mariadb_connection = mariadb.connect(
	user = 'proj127', password='proj127', database = 'project127', host = 'localhost', port = '3306'
)

# used to communicate with the mysql database 
create_cursor = mariadb_connection.cursor(buffered = True, dictionary = True)
#the database return a dictionary

# global variable that holds how many categories there are in the database
categCounter = 0

# function that updates the categCounter to hold the count of all the categories in the database
def categoryCount():
	global categCounter

	select_content = "SELECT category_id FROM category" # query statement
	create_cursor.execute(select_content) # executes the query statement to the database
	mycategories = create_cursor.fetchall() # fecthes all rows of the query result

	categCounter = len(mycategories) # gets the length of mycategories

# function that displays the menu list
def menu():
	print("\nOptions:")
	print("[1]  Create task")
	print("[2]  Edit task")
	print("[3]  Delete task")
	print("[4]  View all task")
	print("[5]  Mark task as done")
	print("[6]  Add category")
	print("[7]  Delete category")
	print("[8]  View category")
	print("[9]  Add task to a category")
	print("[10] Edit Category")
	print("[0]  Exit")
	choice = int(input("Choice: "))
	return choice

# function that checks for the validity of the input date
def dateChecker(deadline):
	year = int(deadline[:4]) # cuts the parameter to take only the year
	month = int(deadline[5:7]) # cuts the parameter to take only the month
	date = int(deadline[8:10]) # cuts the parameter to take only the date
	leap = 0 # variable for checking the leap year

	if year % 4 == 0: # checks if the year is a leap year
		leap = 1 # updates the value of leap to 1
	else: # if year is not a leap year
		leap = 0 # maintain the value of leap = 0

	if month == 2: # if the month is february
		return 28 + leap # adding the value of leap to 28 since if it is leap year, february has 29 days
	
	months31 = [1, 3, 5, 7, 8, 10, 12] # all the months that have 31 days

	if month in months31: # checks if the value of month is inside the list
		return 31 # if true then it returns 31
	
	return 30 # else it returns 30

# function to create a new task
def createTask(task_title, task_details, task_deadline, task_status):
	insert_content = f"INSERT INTO task (title, details, deadline, status) VALUES ('" + task_title + "', '" + task_details + "', STR_TO_DATE('" + task_deadline + "', '%Y/%m/%d'), '" + task_status + "')" # query statement
	create_cursor.execute(insert_content) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database
	print("Succesfully created new Task!") # prompts the user that the task is created successfully

# function to check if id exist
def check_ID(id, table): 
	create_cursor.execute(f"select {table}_id from {table} where {table}_id = '{id}'") # executes the query statement to the database
	
	check_exist = create_cursor.fetchall() # fectches all the result from the query
	if check_exist:
		return True # if the id exists then it returns true
	else:
		print("ID does not exist!") # else it prompts the user that the id does not exist
		return False # returning false

# function that selects all from the 'table' then return a list of dictionary
def selectAll(table):
	select_query = 'SELECT * FROM {}' # query statement
	create_cursor.execute(select_query.format(table)) # executes the query statement to the database

	selected_items = create_cursor.fetchall() # fetches all the matched tuples
	#selected_items is a DICTIONARY
	
	if create_cursor.rowcount == 0:
		print("\n"+ table + " is empty!") # if there are no matches, it prompts the user that the table is still empty
	
	else:
		return selected_items # returns the matched tuples

# function that updates a task
def updateOneTask(col_name, newData, id):
	update_query = "UPDATE task SET " + col_name + " = '"+ newData +"' WHERE task_id = " + str(id) # query statement
	create_cursor.execute(update_query) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database
	print("Task's " + col_name + " with id #" + id + " is updated successfully!") # prompts the user that the task has been updated

# function that deletes a task
def deleteTask(id):
	delete_query = "DELETE FROM task WHERE task_id =" + str(id) # query statement
	create_cursor.execute(delete_query) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database
	print("Task is successfully deleted!") # prompts the user that the task has been deleted

#function that prints all either from task or category table
def printAll(table):
	selected_items = selectAll(table) # calls the selectAll function to get all the matching tuples
	print('\n')
	
	if selected_items != None: # if selected_items has a value

		for x in selected_items:
			for key, value in x.items():
				print(str(key) + ": " +  str(value)) # key: value

			if table=='task':
				id = x["category_id"]

				if id != None:
					create_cursor.execute(f"select name from category where category_id = '{id}'")
					categName = create_cursor.fetchone() #get the query
					name = categName["name"] #get the value
					print(f"Category name: {name}")
				
			print('\n')

# function that creates a category
def createCateg(categ_name, categ_description):
	insert_content = f"INSERT INTO category (name, description) VALUES ('" + categ_name + "', '" + categ_description + "')" # query statement
	create_cursor.execute(insert_content) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database

	print("Succesfully created new Category!") # prompts that the category has been created

#function that edits a category
def editCateg(col_name, newData, id):
    #UPDATE category SET <col_name> = <newData> WHERE task_id = <id> 
	update_query = "UPDATE category SET " + col_name + " = '"+ newData +"' WHERE category_id = " + str(id) #query for editing category
	create_cursor.execute(update_query) #execute the query
	mariadb_connection.commit() #commit
	print("Category's " + col_name + " with id #" + id + " is updated successfully!")
	
# function that deletes a category
def deleteCateg(id):
	delete_tasks = "DELETE FROM task WHERE category_id =" + str(id) # query statement
	create_cursor.execute(delete_tasks) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database

	delete_category= "DELETE FROM category WHERE category_id =" + str(id) # query statement
	create_cursor.execute(delete_category) # executes the query statement to the database
	mariadb_connection.commit() # commits the changes to the database
	print("Category is successfully deleted!") # prompts that the category has been deleted

def viewACategory(categ_id):
	view_query = "SELECT * FROM category JOIN task ON category.category_id = task.category_id WHERE task.category_id =" + str(categ_id)
	create_cursor.execute(view_query)
	result = create_cursor.fetchone()
	
	name = result["name"]
	description = result["description"]
	#tasks = result["task"]
	
	print(f"\nCategory name: {name}")
	print(f"Descriptiom: {description}")
	print(f"Category ID: " + str(categ_id))
	
	create_cursor.execute(f"select title from task where category_id = '{categ_id}'")
	task_name = create_cursor.fetchall()

	if task_name != None:
		print(f"Tasks:")
	
		for x in task_name:
			for key, value in x.items():
				print("\t" + str(value)) # key: value

	else:
		print("No task in this category!")

def addTasktoCategory(task_id, categ_id):
	query = f"UPDATE task SET category_id = '{categ_id}' WHERE task_id = '{task_id}'"
	create_cursor.execute(query)
	mariadb_connection.commit()
	print("Task is successfully added to a category!")

print("\n----------------- Welcome!!! -----------------")
categoryCount()

while True:
	c = menu()

	if c == 0: # exit
		print("\n---- Thank you for using the application! ----")
		break
	
	elif c == 1: # create task
		title = input("\nEnter title of task (must not exceed 15 characters): ") # asks the client to input the title of the task to be created
		details = input("Enter task detail (must not exceed 50 characters): ") # asks the client to input the details of the task to be created

		while True:
			deadline = input("Enter deadline date (format: YYYY/MM/DD): ") # asks the client to input the deadline date of the task to be created

			month = int(deadline[5:7]) # cuts the parameter to take only the month
			date = int(deadline[8:10]) # cuts the parameter to take only the date
			availableDate = dateChecker(deadline) # variable that holds the return value of the function dateChecker

			if month <= 12 and month > 0: # if the month is within 1 - 12
				if date <= availableDate and date > 0: # if date is within 1 - availableDate
					break # stops the while loop
			
			print("Invalid date!") # else it prompts the user that the input date is invalid

		status = "INC" # defaults that the status of a newly created task is incomplete

		createTask(title, details, deadline, status) # creates the task by calling the function createTask
	
	elif c == 2: #edit task
		task_id = input("\nEnter id: ") #asks for an id

		if check_ID(task_id, 'task'): #checks if id exists
			taskTable = selectAll('task') #gets task table
			ctr = 0 #for numbering

			# asks the use which part of the task they want to edit
			print("what do you want to edit:")
			for key in taskTable[0]:
				if key != 'task_id' and key != 'status' and key != 'category_id':
					print(f"\t[{ctr}] {key}")
					ctr += 1

			try:
				choiceNum = int(input("\tChoice: ")) # waits for the user's input

				if choiceNum == 0: # edits the title of the task
					newData = input("\nNew title (must not exceed 15 characters): ")
					colname = 'title'
				elif choiceNum == 1: # edits the details of the task
					newData = input("\nNew task details (must not exceed 50 characters): ")
					colname = 'details'
				elif choiceNum == 2: # edits the deadline of the task
					newData = input("\nNew deadline date (format: YYYY/MM/DD): ")
					colname = 'deadline'	
				else: # prompts that the user chose an invalid input
					print("Invalid Choice!") 
					newData = None

				if newData is not None:
					updateOneTask(colname, newData, task_id) # updates the task
				else:
					print("Unsuccessful edit\n") # prompts that the edit is unsuccessful

			except ValueError: # if the user ever types a character rather than an integer
				print("Invalid Choice!") # prompts that the choice is invalid input
				print("Unsuccessful edit\n") # prompts that the edit is unsuccessful

	elif c == 3: #deletes a task
		task_id = input("\nEnter id: ") # asks the user for a task id

		if check_ID(task_id, 'task'): # checks if the task id is available 
			deleteTask(task_id) # proceeds to delete a task

	elif c == 4: #view all task
		printAll('task')

	elif c == 5: #update status into 'C'
		task_id = input("\nEnter id: ") #ask id

		if check_ID(task_id, 'task'):
			complete = 'C'
			updateOneTask('status', complete, task_id)

	elif c == 6: #creates a category
		categCounter += 1 # increments the categCounter 
		print(categCounter)
		categ_name = input("\nEnter category name (must not exceed 15 characters): ") # asks the client to input the name of the category to be created
		categ_description = input("Enter category description (must not exceed 100 characters): ") # asks the client to input the description of the category to be created

		createCateg(categ_name, categ_description) # calls the createCateg function to make a new category

	elif c == 7: #deletes a category
		category_id = input("\nEnter category id: ")
		if check_ID(category_id, 'category'):
			deleteCateg(category_id)

	elif c == 8: #view all category
		if categCounter > 0:
			print("\n[1] View all category")
			print("[2] View a category")

			try:
				category_choice = int(input("\nChoose an option: "))

				if category_choice == 1:
					printAll('category') #for all
					
				elif category_choice == 2:
					try:
						categ_id = int(input("Enter category id: "))
						#if check_ID(categ_id, 'category'):
						
						if categCounter == 0:
							print("Error: client must first create a category!")
						else: 
							if check_ID(categ_id, 'category'):
								viewACategory(categ_id)

					except ValueError:
						print("Invalid Choice!")

				else: print("Invalid Choice!")

			except ValueError:
				print("Invalid Choice!")
		
		else: 
			print("Error: client must first create a category!")

	elif c == 9: #add task to a category
		# categCounter
		task_id = input("\nEnter task id: ")
		if check_ID(task_id, 'task'):
			
			if categCounter > 0:
				printAll('category')
				categ_id = input("Enter category id: ")
				if check_ID(categ_id, 'category'):
					addTasktoCategory(task_id, categ_id)
			else:
				print("Error: client must first create a category!")
				
	elif c == 10: #edit category
		category_id = input("\nEnter id: ") #asks for an id

		if check_ID(category_id, 'category'): #checks if id exists
			categTable = selectAll('category') #gets category table
			ctr = 0 #for numbering

			# asks the use which part of the category they want to edit
			print("what do you want to edit:")
			for key in categTable[0]:
				if key != 'category_id':
					print(f"\t[{ctr}] {key}")
					ctr += 1

			try:
				choiceNum = int(input("\tChoice: ")) # waits for the user's input

				if choiceNum == 0: # edits the name of the category
					newData = input("\nNew category name (must not exceed 15 characters): ")
					colname = 'name'
				elif choiceNum == 1: # edits the description of the category
					newData = input("\nNew category description (must not exceed 100 characters): ")
					colname = 'description'	
				else: # prompts that the user chose an invalid input
					print("Invalid Choice!") 
					newData = None

				if newData is not None:
					editCateg(colname, newData, category_id) # updates the category
				else:
					print("Unsuccessful edit\n") # prompts that the edit is unsuccessful

			except ValueError: # if the user ever types a character rather than an integer
				print("Invalid Choice!") # prompts that the choice is invalid input
				print("Unsuccessful edit\n") # prompts that the edit is unsuccessful

	else:
		print("invalid input!") # prompts that the choice is invalid input
