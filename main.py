from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

fake_db = {}
counter = 1  

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

class Todo(TodoCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    global counter  
    await asyncio.sleep(0)  
    new_todo = Todo(id=counter, title=todo.title, description=todo.description, completed=False)
    fake_db[counter] = new_todo
    counter += 1  
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    await asyncio.sleep(0)  
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return fake_db[todo_id]

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    await asyncio.sleep(0)  
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    existing_todo = fake_db[todo_id]
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.completed = todo.completed
    fake_db[todo_id] = existing_todo
    return existing_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    await asyncio.sleep(0)
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    del fake_db[todo_id]
    return {"message": "Todo successfully deleted"}