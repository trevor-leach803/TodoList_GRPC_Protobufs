import grpc 
import todo_pb2 as pb2
import todo_pb2_grpc as pb2_grpc
from concurrent import futures


class TodoManagerService(pb2_grpc.TodoManagerServicer):

    def AddTodo(self, request, context):
        # If the request's status is COMPLETED, set the response success to false
        if request.status == 2:
            return pb2.TodoResponse(success=False)
        # If the item already exists in the todo list, set the response success to false
        for i in todoList.items:
            if i.title == request.title:
                return pb2.TodoResponse(success=False)
        # Otherwise, add the new item to the todo list and set the response success to true
        todoList.items.append(pb2.TodoItem(title=request.title,status=request.status))
        return pb2.TodoResponse(success=True)


    def EditTodo(self, request, context):
        in_list = 0
        for i in todoList.items:
            # If the item already exists, update its status
            if i.title == request.title:
                i.status = request.status
                in_list = 1
        # If an item's status is COMPLETED, delete the item from the todo list
        if request.status == 2:
            todoList.items.remove(pb2.TodoItem(title=request.title,status=request.status))
        # If the item does exist and was edited, set the response success to true. Otherwise, set it to false.
        if in_list == 1:
            return pb2.TodoResponse(success=True)
        else: 
            return pb2.TodoResponse(success=False)


    def GetTodos(self, request, context):
        return todoList


    def DelList(self,request,context):
        del todoList.items[:]
        return pb2.empty()


def serve():
    # Establish the server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TodoManagerServicer_to_server(TodoManagerService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == '__main__':
    # Create the todo list that the server will maintain
    todoList = pb2.TodoList()
    # Start the server
    serve()