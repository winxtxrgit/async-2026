# Objective: Compare the structural and mechanical differences of both strategies in a racing scenario.
import asyncio
from time import ctime

async def runner(name, speed):
    await asyncio.sleep(speed)
    return f"{name} crossed line!"

async def main():
    # gather(): รับ coroutine โดยตรง และ "รอทุกตัวจนเสร็จ" คืน list ผลลัพธ์ตามลำดับ input
    print(f"{ctime()} --- Starting gather() approach (Unified Aggregation) ---")
    all_finishes = await asyncio.gather(runner("A", 0.5), runner("B", 2.0))
    print(f"{ctime()} Gather output: {all_finishes}\n")  # รอครบ ~2.0s แล้วได้ผลทั้งคู่

    # wait(): รับเซตของ Task และคุมเงื่อนไขได้ เช่น FIRST_COMPLETED เพื่อทำ racing
    print(f"{ctime()} --- Starting wait() approach (State control / Racing) ---")
    active_tasks = {asyncio.create_task(runner("A", 0.5)), asyncio.create_task(runner("B", 2.0))}

    done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"{ctime()} Wait output: The winner of the race is -> {list(done)[0].result()}")

    # เคลียร์ตัวที่ยังค้าง (pending) ทิ้งเพื่อประหยัดทรัพยากร
    for t in pending:
        t.cancel()

asyncio.run(main())
