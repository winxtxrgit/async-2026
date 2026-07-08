# Objective: Attach a plain synchronous function that automatically triggers the moment a task finishes.
import asyncio
from time import ctime

def alert_manager(finished_task):
    # callback เป็นฟังก์ชันธรรมดา (ไม่ใช่ coroutine) และรับ Task object เข้ามาเป็น argument แรกอัตโนมัติ
    print(f"{ctime()} Callback Triggered! Task output fetched: {finished_task.result()}")

async def download_file():
    print(f"{ctime()} Downloading packet...")
    await asyncio.sleep(1.0)
    return "Data_Payload.zip"

async def main():
    task = asyncio.create_task(download_file())
    # ผูก callback ให้ทำงานทันทีเมื่อ Task เข้าสถานะ "done"
    task.add_done_callback(alert_manager)

    await task  # รอให้ Task เสร็จ (เมื่อเสร็จ event loop จะเรียก alert_manager ให้เอง)

asyncio.run(main())
