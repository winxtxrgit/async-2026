# Program 10: Extracting Return Values from Tasks
# Concept: Accessing returned results from completed Task objects using .result() or direct assignment.

import asyncio
from time import ctime

async def compute(name, value):
    print(f"[{ctime()}] [{name}] คำนวณ {value}²...")
    await asyncio.sleep(1)
    result = value * value
    print(f"[{ctime()}] [{name}] เสร็จ! {value}² = {result}")
    return result

async def main():
    print("=== วิธีที่ 1: รับค่าจาก await โดยตรง (Direct Assignment) ===\n")

    task1 = asyncio.create_task(compute("Task-1", 5))
    task2 = asyncio.create_task(compute("Task-2", 3))

    result1 = await task1   # await คืนค่าที่ return มาโดยตรง
    result2 = await task2
    print(f"\nผลลัพธ์ task1 (direct): {result1}")
    print(f"ผลลัพธ์ task2 (direct): {result2}")

    print("\n" + "=" * 50)
    print("=== วิธีที่ 2: ใช้ .result() หลัง task เสร็จแล้ว ===\n")

    task3 = asyncio.create_task(compute("Task-3", 7))
    task4 = asyncio.create_task(compute("Task-4", 4))

    # รอให้ทั้งคู่เสร็จก่อน (ถ้าเรียก .result() ก่อนเสร็จจะ Exception!)
    await task3
    await task4

    print(f"\nผลลัพธ์ task3 (.result()): {task3.result()}")
    print(f"ผลลัพธ์ task4 (.result()): {task4.result()}")
    print(f"task3.done(): {task3.done()}")
    print(f"task4.done(): {task4.done()}")

asyncio.run(main())

# สรุป:
# วิธีที่ 1 (result = await task)  — นิยมใช้มากกว่า ปลอดภัยกว่า
# วิธีที่ 2 (task.result())        — ใช้ได้แต่ต้องมั่นใจว่า task.done() == True แล้ว
