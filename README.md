# TodoList_GRPC_Protobufs

This project initially served to complete an assignment for CSIS 604 at the College of Charleston.

The server will maintain a to-do list that contains the item title and its status. Once an item's status changes to Completed, the item is removed from the to-do list automatically.

To run:
1. Run todo_server.py
2. Run todo_client.py

The user is provided with 7 options:
1. Running the script with default options (just to show how it works; not really necessary)
2. Take in a text file in format <COMMAND> <TODO ITEM TITLE> <ITEM STATUS> and add them to the list
3. Manually add to-do items to list
4. Edit item status
5. Clear the entire list
6. Print the list
7. Quit the program

This code makes use of protobufs to create the methods for communicating between the client and server. 

Compile the .proto file containing the RPC information using the following at the command line:

python -m grpc_tools.protoc --proto_path=. ./todo.proto --python_out=. --grpc_python_out=.

This is a good example of how to use GRPCs and Protobufs together: https://www.velotio.com/engineering-blog/grpc-implementation-using-python
