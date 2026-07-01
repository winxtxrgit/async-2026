# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.

import asyncio
from time import ctime

async def workflow_a():
    print(f"[{ctime()}] [Workflow-A] ขั้นตอนที่ 1")
    await asyncio.sleep(1)                          # <- event loop สลับไป B
    print(f"[{ctime()}] [Workflow-A] ขั้นตอนที่ 2")
    await asyncio.sleep(1)                          # <- event loop สลับไป B
    print(f"[{ctime()}] [Workflow-A] ขั้นตอนที่ 3 (จบ)")

async def workflow_b():
    print(f"[{ctime()}] [Workflow-B] ขั้นตอนที่ 1")
    await asyncio.sleep(1)                          # <- event loop สลับกลับ A
    print(f"[{ctime()}] [Workflow-B] ขั้นตอนที่ 2")
    await asyncio.sleep(1)                          # <- event loop สลับกลับ A
    print(f"[{ctime()}] [Workflow-B] ขั้นตอนที่ 3 (จบ)")

async def main():
    print(f"[{ctime()}] main() เริ่มต้น")
    print("สังเกต: Thread เดียวสลับไปมาระหว่าง A กับ B ที่ทุก await")
    print("-" * 55)

    task_a = asyncio.create_task(workflow_a())
    task_b = asyncio.create_task(workflow_b())

    await task_a
    await task_b

    print("-" * 55)
    print(f"[{ctime()}] จบ — นี่คือ Cooperative Multitasking บน Single Thread!")

asyncio.run(main())

# สรุป:
# ทุกครั้งที่เจอ await asyncio.sleep() = coroutine นั้นหยุดชั่วคราว
# event loop ฉวยโอกาสรัน coroutine อื่นที่รอคิวอยู่
# นี่คือ "Context Switching" ของ asyncio (ทำเองไม่ใช่ OS ทำ)
