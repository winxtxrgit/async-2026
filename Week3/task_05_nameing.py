# Objective: Label task objects explicitly to simplify logging and production tracking.
import asyncio
from time import ctime

async def background_worker():
    await asyncio.sleep(0.1)

async def main():
    task = asyncio.create_task(background_worker())

    # หากไม่ตั้งชื่อ asyncio จะตั้งชื่อ default ให้เอง เช่น "Task-1"
    print(f"{ctime()} Initial Name: {task.get_name()}")  # -> Task-1

    # กำหนดชื่อที่สื่อความหมายเพื่อช่วยในการ debug / logging
    task.set_name("Payment-Gateway-Validator")
    print(f"{ctime()} Updated Name: {task.get_name()}")  # -> Payment-Gateway-Validator

asyncio.run(main())
