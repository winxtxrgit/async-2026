# Program 5: Sequential Execution (The Wrong Way)
# Concept: Showing that simply awaiting one after another is still sequential (Synchronous behavior).

import asyncio
from time import ctime, time

async def do_task(name, delay):
    print(f"[{ctime()}] [{name}] เริ่มต้น...")
    await asyncio.sleep(delay)
    print(f"[{ctime()}] [{name}] เสร็จแล้ว!")

async def main():
    start = time()

    print("=== await ทีละงาน (ยังคงเป็น Sequential!) ===\n")

    # แม้จะใช้ async/await แต่ถ้า await ทีละงาน = ยังเป็น Sequential อยู่!
    await do_task("งาน A", 1)
    await do_task("งาน B", 1)
    await do_task("งาน C", 1)

    elapsed = time() - start
    print(f"\nใช้เวลาทั้งหมด: {elapsed:.2f} วินาที")
    print("สังเกต: ใช้เวลา ~3s ไม่ใช่ ~1s!")
    print("นี่คือ 'The Wrong Way' ถ้าต้องการให้รันพร้อมกัน")
    print()
    print("วิธีแก้: ใช้ asyncio.create_task() ก่อน แล้วค่อย await")
    print("        หรือใช้ asyncio.gather() รวมทีเดียว")

asyncio.run(main())
