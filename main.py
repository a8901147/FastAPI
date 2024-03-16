from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    text: str
    status: int = 0   

class TaskCreate(BaseModel):
    text: str


tasks: List[Task] = [Task(id=1, text="task", status=0)]
# there is a potential Race Condition issue if lack of async lock
# with the async lock might also cause performance issue
# the id generation duplicate issue generally can be solved by DB
tasks_new_id = len(tasks)+1
lock = asyncio.Lock()  # Create a lock

@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    return tasks

@app.post("/task", response_model=Task, status_code=201)
async def create_task(task_create: TaskCreate):
    global tasks_new_id
    # Use the lock to ensure exclusive access to tasks_new_id
    async with lock:
        task = Task(id=tasks_new_id, text=task_create.text, status=0)
        tasks_new_id += 1
    tasks.append(task)
    return task

@app.put("/task/{task_id}", response_model=Task, status_code=200)
async def update_task(task_id:int, updated_task: Task):
    if task_id != updated_task.id:
        raise HTTPException(status_code=403, detail="the task_id is not matched with the body.data_id")
    
    # when dealing with big data, we might consider indexing id column in SQL or key value store in key-value
    # storage in NoSQL 
    for task in tasks:
        if task.id == task_id:
            task.text = updated_task.text
            task.status = updated_task.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/task/{task_id}", status_code=200)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return 
    raise HTTPException(status_code=404, detail="Task not found")