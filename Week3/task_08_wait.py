# Objective: Implement complex processing workflows based on task fulfillment conditions.
import asyncio
from time import ctime

async def network_probe(server_name, delay):
    await asyncio.sleep(delay)
    return f"Ping successful: {server_name}"

async def main():
    # wait() รับ "เซตของ Task objects" (ไม่ใช่ coroutine ดิบ ๆ)
    tasks = {
        asyncio.create_task(network_probe("Primary-Server", 2.0)),
        asyncio.create_task(network_probe("Backup-Server-1", 0.5)),
        asyncio.create_task(network_probe("Backup-Server-2", 1.0))
    }

    # FIRST_COMPLETED -> คืนทันทีเมื่อมีตัวแรกเสร็จ และแยกออกเป็น 2 เซต: done / pending
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    print(f"{ctime()} Count of Tasks Done: {len(done)}")        # 1 -> ตัวที่เร็วสุด (0.5s)
    print(f"{ctime()} Count of Tasks Pending: {len(pending)}")  # 2 -> ที่เหลือยังทำงานค้าง

    for finished_task in done:
        print(f"{ctime()} Fastest Task Result: {finished_task.result()}")

    # ยกเลิกงานที่ยังค้าง (pending) เพื่อไม่ให้รันทิ้งเปล่าและป้องกัน memory leak
    for ongoing_task in pending:
        ongoing_task.cancel()

asyncio.run(main())
