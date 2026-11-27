from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title='Task Manager API')

class Task(BaseModel):
    title: str
    completed: bool = False

task_db = {}
current_id = 1


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global current_id
    if not task.title.strip():
        raise HTTPException(status_code=400, detail='Название не найдено!')
    new_task = {'id': current_id, 'title': task.title, 'completed': task.completed}
    task_db[current_id] = new_task
    current_id += 1
    return new_task


@app.get("/tasks")
def get_all_tasks():
    return list(task_db.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail='Таск не найден!')
    return task_db[task_id]


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail='Таск не найден!')
    
    task_db[task_id]['title'] = task.title
    task_db[task_id]['completed'] = task.completed
    return task_db[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail='Таск не найден!')
    del task_db[task_id]
