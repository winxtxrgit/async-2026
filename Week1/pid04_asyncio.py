from time import ctime, time
import asyncio
import os
import threading

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name} "
          f"| PID={os.getpid()} | Thread={threading.current_thread().name}")
    await asyncio.sleep(2)  # จำลองเวลาชงกาแฟ 2 วินาที (ไม่บล็อก event loop)
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕ | PID={os.getpid()}")

async def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]
    print(f"โปรแกรมหลักทำงานที่ PID={os.getpid()}\n")

    start = time()

    # asyncio: ทุก task รันบน PID และ Thread เดียวกัน (MainThread) แต่สลับกันทำงาน
    await asyncio.gather(*(make_coffee(c) for c in customers))

    end = time()
    print(f"\nเสร็จทั้งหมด {len(customers)} คน | ใช้เวลา {end - start:.2f} วินาที")

if __name__ == "__main__":
    asyncio.run(main())
