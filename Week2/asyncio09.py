# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.

import asyncio
from time import ctime, time

async def process_item(item_id, delay):
    print(f"[{ctime()}] [Item-{item_id}] เริ่มประมวลผล (delay={delay}s)...")
    await asyncio.sleep(delay)
    print(f"[{ctime()}] [Item-{item_id}] เสร็จสิ้น!")
    return f"Item-{item_id} processed"

async def main():
    start = time()

    # ข้อมูล items พร้อม delay ของแต่ละชิ้น
    items = [("A", 1), ("B", 2), ("C", 1), ("D", 3), ("E", 1)]

    print(f"=== สร้าง {len(items)} tasks แบบ dynamic (loop + append) ===\n")

    # สร้าง tasks ทั้งหมดก่อน แล้วเก็บลง list
    tasks = []
    for item_id, delay in items:
        task = asyncio.create_task(process_item(item_id, delay))
        tasks.append(task)

    print(f"สร้าง tasks ทั้งหมด {len(tasks)} tasks แล้ว (ทุก task เริ่มนับเวลาพร้อมกัน)")
    print("-" * 55)

    # รอทุก task เสร็จ แล้วเก็บผลลัพธ์
    results = []
    for task in tasks:
        result = await task
        results.append(result)

    print("-" * 55)
    print("\nผลลัพธ์ทั้งหมด:")
    for r in results:
        print(f"  - {r}")

    print(f"\nใช้เวลาทั้งหมด: {time()-start:.2f}s (เทียบกับ {sum(d for _, d in items)}s ถ้าทำ Sequential)")

asyncio.run(main())
