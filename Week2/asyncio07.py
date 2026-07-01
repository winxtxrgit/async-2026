# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.

import asyncio
from time import ctime, time

async def task_alpha(delay):
    print(f"[{ctime()}] [Alpha] เริ่ม (จะใช้เวลา {delay}s)")
    await asyncio.sleep(delay)
    print(f"[{ctime()}] [Alpha] เสร็จสิ้น!")
    return "Alpha Done"

async def task_beta(delay):
    print(f"[{ctime()}] [Beta] เริ่ม (จะใช้เวลา {delay}s)")
    await asyncio.sleep(delay)
    print(f"[{ctime()}] [Beta] เสร็จสิ้น!")
    return "Beta Done"

async def main():
    start = time()
    print("=== สร้าง 2 Tasks พร้อมกัน (ไม่ใช้ gather) ===\n")

    # สร้าง 2 tasks พร้อมกันก่อน (ทั้งคู่เริ่มนับเวลาพร้อมกัน)
    t1 = asyncio.create_task(task_alpha(2))
    t2 = asyncio.create_task(task_beta(1))

    # await ทีละอัน (beta เสร็จก่อน แต่ alpha ก็รันอยู่ตลอด)
    result1 = await t1
    result2 = await t2

    print(f"\nผลลัพธ์ 1: {result1}")
    print(f"ผลลัพธ์ 2: {result2}")
    print(f"ใช้เวลาทั้งหมด: {time()-start:.2f}s  (ไม่ใช่ 3s แต่ ~2s เพราะทำงานพร้อมกัน)")

asyncio.run(main())

# สรุป:
# สร้าง task ทั้ง 2 ก่อน แล้วค่อย await = ทั้งคู่นับเวลาพร้อมกัน
# ถ้า await t1 แล้วค่อย create t2 = ยังคง Sequential อยู่
