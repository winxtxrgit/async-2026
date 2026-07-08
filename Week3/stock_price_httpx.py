# stock_price_httpx.py (เวอร์ชันสำหรับแจกเป็นโจทย์หรือแนวทางให้นักเรียนเขียน)
import asyncio
import httpx  
from time import ctime

async def fetch_stock_price(server_name: str):
    """
    TODO: Assignment 3 - เขียนฟังก์ชันเชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    1. กำหนดเป้าหมายไปที่พอร์ต 8088 ตามสเปกเซิร์ฟเวอร์ของอาจารย์
    2. ใช้ httpx.AsyncClient() ดึงข้อมูลเพื่อไม่ให้เกิดการ Block สัญญาณ Event Loop
    3. นำข้อมูล JSON (server และ price_usd) มาจัดฟอร์แมตแสดงผล
    """
    url = f"http://127.0.0.1:8088/price/{server_name}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            return f"[{data['server']}] Price: {data['price_usd']} USD"
    except httpx.ConnectError:
        # ต่อเซิร์ฟเวอร์ไม่ได้ (ยังไม่เปิด uvicorn / ผิดพอร์ต) -> คืนข้อความชัดเจนแทน traceback
        return (f"[{server_name}] ERROR: เชื่อมต่อเซิร์ฟเวอร์ไม่ได้ "
                f"(ตรวจว่าเปิด uvicorn stock_api:app --port 8088 อยู่หรือไม่)")
    except httpx.HTTPError as e:
        # error อื่น ๆ จาก httpx เช่น timeout / อ่านข้อมูลไม่สำเร็จ
        return f"[{server_name}] ERROR: {type(e).__name__} - {e}"

async def main():
    """
    จัดการส่งกลุ่ม Tasks ทำ Concurrency Racing บนเซิร์ฟเวอร์ย่อย Alpha, Beta, Gamma
    และปิดกั้นทรัพยากรตัวที่ค้างคา (pending) ทิ้งทันทีเมื่อมีผู้ชนะ
    """
    # แปลงคอรูทีนของทั้ง 3 สาขาให้เป็น asyncio.Task เพื่อรันพร้อมกันใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha"), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta"), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma"), name="Gamma"),
    }

    print(f"{ctime()} Racing 3 servers... (waiting for the fastest)")

    # ใช้ asyncio.wait() + FIRST_COMPLETED เพื่อดีดตัวออกทันทีเมื่อมีตัวแรกสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # ดึงผลลัพธ์จากเซิร์ฟเวอร์ที่ชนะการแข่งขัน (เร็วที่สุด) ออกมาแสดงผล
    for winner in done:
        print(f"{ctime()} WINNER -> {winner.result()}")

    # [Anti-Memory Leak] ยกเลิกงานที่ยังค้างอยู่ใน pending ทั้งหมด เพื่อตัด Network Request ที่ยังวิ่งค้าง
    print(f"{ctime()} Cleaning up {len(pending)} pending task...")
    for ongoing_task in pending:
        ongoing_task.cancel()

    # รอให้งานที่ถูกยกเลิกจบจริง ๆ (กลืน CancelledError ไม่ให้ค้าง)
    await asyncio.gather(*pending, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
