from time import ctime, time
import asyncio

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name}")
    await asyncio.sleep(2)  # จำลองเวลาชงกาแฟ 2 วินาที (ไม่บล็อก event loop)
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕")

async def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    start = time()

    # ทำงานแบบ async: สร้าง task ของลูกค้าทุกคน แล้วรอพร้อมกันด้วย gather
    tasks = [make_coffee(customer) for customer in customers]
    await asyncio.gather(*tasks)

    end = time()
    print(f"\nทำกาแฟให้ลูกค้าทั้งหมด {len(customers)} คน เสร็จสิ้น")
    print(f"ใช้เวลารวมทั้งหมด {end - start:.2f} วินาที")

# สั่งให้ระบบ Async เริ่มทำงาน
if __name__ == "__main__":
    # ใช้ asyncio.run เพื่อเปิด Event Loop หลักของโปรแกรม
    asyncio.run(main())
