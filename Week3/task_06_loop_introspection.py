# Objective: Introspect runtime contexts and monitor open workload queues on the active loop.
import asyncio
from time import ctime

async def dynamic_job(number):
    await asyncio.sleep(1.0)

async def main():
    # current_task() คืน Task ที่กำลังรันอยู่ ณ ตอนนี้ (ก็คือตัว main เอง)
    me = asyncio.current_task()
    me.set_name("Main-Coordinator")
    print(f"{ctime()} Active Execution Context Name: {me.get_name()}")

    # แตกงานย่อยขึ้นมา 3 ตัว พร้อมตั้งชื่อ Job-0, Job-1, Job-2
    tasks = [asyncio.create_task(dynamic_job(i), name=f"Job-{i}") for i in range(3)]

    # all_tasks() คืน set ของ Task ทั้งหมดที่ยังทำงานไม่เสร็จบน event loop (รวม main ด้วย = 4 ตัว)
    all_active = asyncio.all_tasks()
    print(f"{ctime()} Total Active Tasks inside Loop: {len(all_active)}")
    for t in all_active:
        print(f"{ctime()}  -> Active Queue Item: {t.get_name()}")

    await asyncio.sleep(1.1)  # รอให้ job ย่อยทั้งหมด (sleep 1.0s) ทำงานเสร็จก่อนจบโปรแกรม

asyncio.run(main())
