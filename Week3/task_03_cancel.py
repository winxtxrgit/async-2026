# Objective: Stop an ongoing execution prematurely by triggering a cancellation exception.
import asyncio
from time import ctime

async def background_loop():
    try:
        print(f"{ctime()} Worker: Starting long infinite process...")
        while True:
            await asyncio.sleep(1)  # จุด await นี้คือที่ที่ CancelledError จะถูกฉีดเข้ามา
            print(f"{ctime()} Worker: Still ticking...")
    except asyncio.CancelledError:
        # ดักจับสัญญาณยกเลิกเพื่อทำความสะอาดทรัพยากรก่อนออกจากงาน
        print(f"{ctime()} Worker: Interrupted! Executing clean-up logic before exit...")

async def main():
    task = asyncio.create_task(background_loop())
    await asyncio.sleep(2.5)  # ปล่อยให้ worker วิ่งไปสักพัก (~2 รอบ) ก่อนสั่งยกเลิก

    print(f"{ctime()} Main: Changing plans, canceling the worker task now!")
    task.cancel()          # ส่งคำขอยกเลิก -> ฉีด CancelledError เข้าไปที่ await point
    await asyncio.sleep(0.1)  # คืนคิวให้ event loop เพื่อให้ worker ได้รัน clean-up จริง

asyncio.run(main())
