# Program 6: Creating a Concurrent Task
# Concept: Wrapping a coroutine inside asyncio.create_task() to schedule it to run in the background.

import asyncio
from time import ctime, time

async def background_job(name, delay):
    print(f"[{ctime()}] [{name}] เริ่มงาน background...")
    await asyncio.sleep(delay)
    print(f"[{ctime()}] [{name}] งาน background เสร็จแล้ว!")
    return f"{name} complete"

async def main():
    start = time()

    print(f"[{ctime()}] main() เริ่มต้น\n")

    # create_task() = บอก event loop ให้กำหนดการณ์ coroutine นี้ไว้
    # แต่ยังไม่รันทันที จะรันเมื่อ event loop มีโอกาส (ตอนที่ main หยุด await)
    task = asyncio.create_task(background_job("Task-1", 2))

    print(f"[{ctime()}] Task ถูกสร้างแล้ว (แต่ยังไม่เริ่มรัน)")
    print(f"[{ctime()}] main() กำลังทำงานอื่นอยู่...")

    # await asyncio.sleep(0) = ยอมสละ control ให้ event loop เพื่อให้ task ได้เริ่ม
    await asyncio.sleep(0.5)
    print(f"[{ctime()}] main() ทำงานอื่นเสร็จแล้ว รอ task...")

    # await task = รอจนกว่า task จะเสร็จ แล้วรับผลลัพธ์
    result = await task
    print(f"\n[{ctime()}] ผลลัพธ์: {result}")
    print(f"ใช้เวลาทั้งหมด: {time()-start:.2f}s")

asyncio.run(main())

# สรุป:
# asyncio.create_task(coro)  ≠  await coro
# - await coro        : รัน coro ทันที รอจบแล้วค่อยไปต่อ (Sequential)
# - create_task(coro) : กำหนดการณ์ coro ไว้ ให้รันพร้อมกับงานอื่นได้ (Concurrent)
