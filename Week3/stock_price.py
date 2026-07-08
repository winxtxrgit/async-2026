# นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED เท่านั้น (หากใครใช้ gather หรือ wait_for จะไม่ตรงสเปกเงื่อนไขการแข่งส่งข้อมูล)
import asyncio
from time import ctime


async def fetch_stock_price(server_name, delay):
    """จำลองการดึงราคาหุ้นจากเซิร์ฟเวอร์ โดยแต่ละสาขามี latency ไม่เท่ากัน"""
    print(f"{ctime()} [{server_name}] Connecting... (latency {delay}s)")
    await asyncio.sleep(delay)
    print(f"{ctime()} [{server_name}] Responded!")
    return f"[{server_name}] Price: 150 USD"


async def main():
    # แตก Task ขึ้นมา 3 ตัวพร้อมกันใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Gamma"),
    }

    # ใช้ asyncio.wait() + FIRST_COMPLETED เพื่อดีดตัวออกทันทีเมื่อมีตัวแรกสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน (เร็วที่สุด)
    for winner in done:
        print(f"{ctime()} WINNER -> {winner.result()}")

    # วนลูปเคลียร์ระบบ: ยกเลิกงานของเซิร์ฟเวอร์อีก 2 ตัวที่ยังค้างอยู่ (pending)
    print(f"{ctime()} Cleaning up {len(pending)} pending task(s) to prevent memory leak...")
    for ongoing_task in pending:
        ongoing_task.cancel()

    # รอให้งานที่ถูกยกเลิกจบจริง ๆ (กลืน CancelledError)
    await asyncio.gather(*pending, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
