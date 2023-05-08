from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    title: str
    description: str
    level: str


class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None


todos = {
    0: Todo(title="Sleep", description="Sleep on time", level="Failed"),
    1: Todo(title="Take a Shower", description="Morning shower before work", level="Completed"),
    2: Todo(title="Cook Breakfast", description="Get some of that energy", level="Completed"),
    3: Todo(title="Do Laundry", description="Clean your clothes", level="Incomplete"),
    4: Todo(title="Taxes", description="File taxes report to IRS", level="Incomplete")
}


# GET method = Confirm that the system is running
@app.get("/")
def index():
    return {"Welcome!": "An API for all your To-Do list wonder."}


# GET method = Finding task by matching ID
@app.get("/get-to-do-by-id/{id}")
def get_todo(id: int = Path(description="Search that utilizes the To-Do ID as the parameter")):
    return todos[id]


# GET method = Finding task by matching title
@app.get("/get-to-do-by-title/{title}")
def get_todo_by_title(title: str = Path(description="Search that utilizes the To-Do title as the parameter")):
    for todo_id in todos:
        if todos[todo_id].title == title:
            return todos[todo_id]
    return {"error.exe": "Task does not exist!"}


# GET method = Finding task depending on their level of completion
@app.get("/get-to-do-by-level/{level}")
def get_todo_by_level(level: str = Path(description="Search that utilizes the To-Do level as the parameter")):
    for todo_id in todos:
        if todos[todo_id].level == level:
            return todos[todo_id]
    return {"error.exe": "Level does not exist!"}


# POST method = Create a new To-Do assignment
@app.post("/create-to-do/{todo_id}")
def add_todo(todo_id: int, todo: Todo):
    if todo_id in todos:
        return {"error.exe": "Task already exist!"}
    todos[todo_id] = todo
    return todos[todo_id]


# PUT method = Updating the To-Do list
@app.put("/update-to-do/{todo_id}")
def update_todo(todo_id: int, todo: UpdateTodo):
    if todo_id not in todos:
        return {"error.exe": "Task failed to be added"}
    if todo.title != None:
        todos[todo_id].title = todo.title
    if todo.description != None:
        todos[todo_id].description = todo.description
    if todo.level != None:
        todos[todo_id].level = todo.level
    return todos[todo_id]


# DELETE method = Deleting a To-Do assignment
@app.delete("/delete-to-do/{todo_id}")
def delete_todo(todo_id: int = Path(description="Search the task to be removed")):
    if todo_id not in todos:
        return {"error.exe": "Task does not exist!"}
    del todos[todo_id]
    return {"succeed!": "Task has been removed"}
