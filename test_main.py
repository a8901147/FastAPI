import pytest
from httpx import AsyncClient
import asyncio
from main import app 

@pytest.mark.asyncio
async def test_list_tasks():
    # mimic the request on testserver without stale the data
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tasks")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_task():
    # mimic the request on testserver without stale the data
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Prepare and send multiple concurrent task creation requests
        tasks_to_create = 100  # This can be adjusted based on your testing needs
        tasks_data = [{"text": f"Test task {i}"} for i in range(tasks_to_create)]
        
        # Send concurrent POST requests without the protective lock
        responses = await asyncio.gather(*(ac.post("/task", json=task_data) for task_data in tasks_data))
        
        # Assuming all responses should be successful; adjust as needed based on your API's design
        assert all(response.status_code == 201 for response in responses), "Not all create task requests were successful"
        
        # Check for duplicate IDs which indicate a race condition
        tasks = [response.json() for response in responses]
        assert all(tasks[i]['status'] == 0 and tasks[i]['text'] == "Test task {}".format(i) for i in range(tasks_to_create))
        task_ids = [task['id'] for task in tasks]
        unique_task_ids = set(task_ids)
        assert len(unique_task_ids) == tasks_to_create, f"Duplicate IDs found: expected {tasks_to_create} unique IDs, but got {len(unique_task_ids)}"

@pytest.mark.asyncio
async def test_update_task():
    updated_task = {"id": 1,"text": "updated task", "status": 1}
    # mimic the request on testserver without stale the data
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/task/1", json=updated_task)
    assert response.status_code == 200
    task = response.json()
    assert task['text'] == "updated task"
    assert task['status'] == 1
    assert task['id'] == 1

@pytest.mark.asyncio
async def test_delete_task():
    task_id = 1
    # mimic the request on testserver without stale the data
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/task/{}".format(task_id))
    assert response.status_code == 200