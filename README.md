CMSC 127 PROJECT By:
    
    Alexa Cordero
    Brixter Sien Pineda 
    Vincent Rodriguez

The requires the following:

    A terminal for the python code
        main.py
    and MariaDB Command Prompt for creating the DATABASE
        proj127.sql

Task Record System:
    A simplified version of a task listing app where you can list a task and put it in a category

App features: 

    Create Task 
    Edit Task 
    Delete Task 
    View Task (all) 
    Mark task as done 
    Add category (e.g., academic, org-related, lovelife, money, to_watch) 
    Edit category 
    Delete category 
    View category 
    Add a task to a category


In create task:
    Choose option 1 for Create Task

    The app asks you for:
        Title (must not exceed 15 characters)
        Detail (must not exceed 50 characters)
        Deadline date (format: YYYY/MM/DD)

    The task's id is based on the order of created tasks
        e.g The first task you create will have '1' as an id
            The second task will have 2 and so on.

    The status will be empty until you mark it as done.


In edit task:
    Choose option 2 for Edit Task

    The app will ask you to enter the task id of the task you want to edit.
    You may edit the title, details, or deadline of the task.

    A menu will show. If you choose...
        0 - you will edit the title
        1 - you will edit the details
        2 - you will edit the deadline

    If id is not found, the app will show 'ID does not exist'


In delete task:
    Choose option 3 for Delete Task

    The app will ask you to enter the task id of the task you want to delete.

    If id is not found, the app will show 'ID does not exist'


In view all task:
    Choose option 4 for View All Task
    
    It will then print all the tasks.

    'Task is empty' is printed if there is no task created.


In mark task as done:
    Choose option 5 for Delete Task

    The app will ask you to enter the task id of the task you want to mark as done.

    If id is not found, the app will show 'ID does not exist'


In add category:
    Choose option 6 for Add category

    The app will show you how many categories created.

    It will then ask you...
        Category name (must not exceed 15 characters)
        Description (must not exceed 100 characters)

    It will show 'Succesfully created new Category!' after you created a category.


In delete category:
    Choose option 7 for Delete Category

    The app will ask you to enter the category id of the category you want to delete.

    If id is not found, the app will show 'ID does not exist'


In view category:
    Choose option 8 for View Category
    
    The app will let you choose 2 options
        1 - View all category
            Here, you can view all categories created. If there is none, a prompt saying 'client must first create a category!' will show.

        2 - View a category
            Here, the app will ask the id of the category you want to view.
            It will show the id, name, description of the category and the tasks under it if there is any.


In add a task to a category:
    Choose option 9 for Add Task to a Category

    The app will ask you to enter the task id of the id you want to add to a task.
    Then it will ask you for the category id.

In edit category:
    Choose option 10 for Edit Category

    A menu will show. If you choose...
        0 - you will edit the title
        1 - you will edit the details

In exit:
    Choose 0 to exit the app.
