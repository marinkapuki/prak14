from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from models import Todo

app = FastAPI()

# Модель для создания нового элемента Todo
class TodoCreate(BaseModel):
    title: str
    description: str

# Модель для обновления элемента Todo
class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

# Подключение к базе данных
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",  # Использует SQLite в качестве базы данных
    modules={"models": ["models"]},  # Укажите, где находятся ваши модели
    generate_schemas=True,  # Генерация схемы базы данных автоматом
    add_exception_handlers=True,  # Перехват исключений Tortoise
)

# Создание элемента Todo
@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    todo_obj = await Todo.create(
        title=todo.title, 
        description=todo.description
    )
    return todo_obj

# Получение элемента Todo по ID
@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    todo_obj = await Todo.filter(id=todo_id).first()
    if todo_obj is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_obj

# Обновление элемента Todo по ID
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    todo_obj = await Todo.filter(id=todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_obj.title = todo_update.title
    todo_obj.description = todo_update.description
    todo_obj.completed = todo_update.completed
    
    await todo_obj.save()  # Асинхронное сохранение обновляемого объекта
    return todo_obj

# Удаление элемента Todo по ID
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo_obj = await Todo.filter(id=todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    await todo_obj.delete()  # Асинхронное удаление объекта из базы данных
    return {"message": "Todo deleted successfully"}
