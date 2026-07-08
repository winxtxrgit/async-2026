# Objective: Extract returned data safely and inspect crashed tasks without breaking the main loop.
import asyncio
from time import ctime

async def division_worker(a, b):
    await asyncio.sleep(0.5)
    return a / b  # ถ้า b เป็น 0 จะเกิด ZeroDivisionError ภายใน Task โดยไม่ทำให้ main พัง

async def main():
    task_success = asyncio.create_task(division_worker(10, 2))  # งานที่หารได้ปกติ
    task_fail = asyncio.create_task(division_worker(10, 0))     # งานที่จะเกิด exception

    # รอให้ทั้งสอง Task ทำงานเสร็จ (แต่ละตัว sleep 0.5s จึงรอ 1s ให้ชัวร์)
    await asyncio.sleep(1)

    # ถ้า Task เสร็จและไม่มี exception ค่อยเรียก .result() ได้อย่างปลอดภัย
    if task_success.done() and not task_success.exception():
        print(f"{ctime()} Task Success Result: {task_success.result()}")  # ดึงค่าผลลัพธ์ที่ return

    # ตรวจ Task ที่พังโดยใช้ .exception() เพื่อดึงตัว exception ออกมาโดยไม่ raise ใส่ main
    if task_fail.done():
        print(f"{ctime()} Task Fail Exception: {type(task_fail.exception()).__name__}")  # -> ZeroDivisionError

asyncio.run(main())
