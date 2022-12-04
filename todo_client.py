import grpc 
import todo_pb2 as pb2
import todo_pb2_grpc as pb2_grpc
import os
from textwrap import dedent
from time import sleep

class TodoManager(object):
    def __init__(self):
        # Establish the connection with the server
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pb2_grpc.TodoManagerStub(self.channel)


    def no_input(self):
        # If no input file is provided, use these for an example of functionality
        self.stub.AddTodo(pb2.TodoItem(title='first_item', status=pb2.TodoItem.NOT_STARTED))
        self.stub.AddTodo(pb2.TodoItem(title='second_item', status=pb2.TodoItem.NOT_STARTED))
        self.stub.AddTodo(pb2.TodoItem(title='third_item', status=pb2.TodoItem.IN_PROGRESS))

        print('To-do list items added.')
        sleep(2)
        client.clear_screen()


    def user_input(self):
        add_more = 'Y'
        self.clear_screen()
        self.print_todos()

        while add_more.upper() == 'Y' or add_more.upper() == 'YES':
            in_title = input('Enter a to-do item: ')
            if not in_title:
                break
            while True:
                item_started = input('Has the to-do item been started? Y/N: ')
                if item_started.upper() == 'Y' or item_started.upper() == 'YES':
                    in_status = pb2.TodoItem.IN_PROGRESS
                    break
                elif item_started.upper() == 'N' or item_started.upper() == 'NO':
                    in_status = pb2.TodoItem.NOT_STARTED
                    break
                else:
                    print('Invalid input. Enter Y or N.')
            
            if not self.stub.AddTodo(pb2.TodoItem(title=in_title, status=in_status)).success:
                print('To-do item already exists.')

            self.clear_screen()
            self.print_todos()
            add_more = input('Do you want to add more to-do items? Y/N: ')
        
        self.clear_screen()


    def update_item(self):
        while True:
            self.clear_screen()
            self.print_todos()
            edit_title = input('Input the title of the to-do item to update: ')
            if not edit_title:
                self.clear_screen()
                return
            edit_status = input(dedent('''\
                What is the new status of the to-do item?
                1. Not started
                2. In progress
                3. Completed

                Status: '''))

            while not edit_status or int(edit_status) < 0 or int(edit_status) > 3:
                if not edit_status:
                    self.clear_screen()
                    return
                print('Invalid input')
                edit_status = input('Select a status number from the above list: ')

            if edit_status == '1':
                edit_status = pb2.TodoItem.NOT_STARTED
            elif edit_status == '2':
                edit_status = pb2.TodoItem.IN_PROGRESS
            elif edit_status == '3':
                edit_status = pb2.TodoItem.COMPLETED

            if not self.stub.EditTodo(pb2.TodoItem(title=edit_title.lower(), status=edit_status)).success:
                print('Item is not in to-do list.')
                sleep(2)
                break

        self.clear_screen()
            
    
    def file_input(self):
        self.clear_screen()
        test_file = input('\nEnter the file name of todo items (include .txt): ')
        if not test_file:
            print('No input file received.')
        else:
            try:
                self.file_provided(test_file)
                print('To-do list items added.')
            except:
                print('\nNo such file in the current working directory.')
        sleep(2)
        self.clear_screen()


    def file_provided(self, file_path):
        # If an input file is provided, parse through it to get commands, titles, and statuses
        with open(file_path) as testfile:
            split_lines = []
            lines = testfile.readlines()
            for line in lines:
                split_lines.append(line.split())

        # For each line in the file, run the respective command
        for line in split_lines:
            input_title = line[1]
            input_status = line[2]
            # Convert the string status so it can be sent to the server
            if input_status == 'NOT_STARTED':
                input_status = pb2.TodoItem.NOT_STARTED
            elif input_status == 'IN_PROGRESS':
                input_status = pb2.TodoItem.IN_PROGRESS
            elif input_status == 'COMPLETED':
                input_status = pb2.TodoItem.COMPLETED

            if line[0] == 'add':
                res = self.stub.AddTodo(pb2.TodoItem(title=input_title, status=input_status)).status
                if res == False:
                    print("Failed to add '{}' to the todo list".format(input_title))
            elif line[0] == 'edit':
                res = self.stub.EditTodo(pb2.TodoItem(title=input_title, status=input_status)).status
                if res == False:
                    print("Failed to edit '{}' on the todo list".format(input_title))
            else:
                print("Invalid input file -- bad status type: '{}'".format(line[0]))


    def print_todos(self):
        # Print the list of todos
        todo_list = self.stub.GetTodos(pb2.empty())
        if len(todo_list.items) == 0:
            print('To-do list is empty.')
            sleep(2)
            self.clear_screen()
            return
        index = 1
        self.clear_screen()
        print('\nTo-Do List')
        for i in todo_list.items:
            # Match status from todo list with string. Python does not have a quick way to do so.
            if i.status == 0:
                status = 'NOT_STARTED'
            elif i.status == 1:
                status = 'IN_PROGRESS'
            elif i.status == 2:
                status = 'COMPLETED'
            # Print final message
            print("{}. {} with status {}".format(index,i.title.upper(),status))
            index += 1
        print('\n')


    def clear_list(self):
        self.stub.DelList(pb2.empty())
        print('To-do list cleared.\n')
        sleep(2)
        self.clear_screen()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

def main(client):
    # Establish the client and server connection
    while True:
        option = input(dedent('''\
            Enter the number of what you would like to do:
            1. Add default to-do items
            2. Add to-do items from a text file
            3. Add to-do items manually
            4. Edit to-do item status
            5. Clear to-do list
            6. Print to-do list
            7. Quit

            Your selection: '''))

        while not option or int(option) < 1 or int(option) > 7:
            print('Invalid entry.')
            option = input('Please select an option from the above list: ')

        if option == '1':
            client.no_input()
        elif option == '2':
            client.file_input()
        elif option == '3':
            client.user_input()
        elif option == '4':
            client.update_item()
        elif option == '5':
            client.clear_list()
        elif option == '6':
            client.print_todos()
        elif option == '7':
            break

    # Print todo list
    client.clear_screen()
    client.print_todos()


if __name__ == '__main__':
    client = TodoManager()
    client.clear_screen()
    main(client)