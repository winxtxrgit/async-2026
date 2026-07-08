# Objective: Learn how to query the lifecycle status of a task object.
import asyncio
from time import ctime

async def short_job():
    await asyncio.sleep(1)
    return "Success"

async def main():
    task = asyncio.create_task(short_job())

    # ตรวจสอบสถานะทันทีหลังสร้าง Task (ยังไม่ทันได้รัน จึงยังไม่ done และยังไม่ถูก cancel)
    print(f"{ctime()} Is task done? {task.done()}")           # False -> ยังทำงานไม่เสร็จ
    print(f"{ctime()} Is task canceled? {task.cancelled()}")  # False -> ยังไม่ถูกยกเลิก

    await task  # รอให้ Task ทำงานจนเสร็จก่อน แล้วค่อยไปตรวจสถานะอีกครั้ง

    # Inspect status again after it finishes
    print(f"{ctime()} Is task done now? {task.done()}")          # True -> ทำงานเสร็จเรียบร้อย
    print(f"{ctime()} Is task canceled now? {task.cancelled()}") # False -> จบแบบปกติ ไม่ได้ถูกยกเลิก

asyncio.run(main())
