# Program 4: The await Keyword
# Concept: Pausing a coroutine to let another operation finish using await.

import asyncio
from time import ctime, time

async def brew_coffee(customer):
    print(f"[{ctime()}] เริ่มชงกาแฟให้ {customer}...")
    await asyncio.sleep(2)   # หยุด (pause) รอ 2 วินาที แต่ไม่บล็อก event loop
    print(f"[{ctime()}] กาแฟของ {customer} เสร็จแล้ว!")
    return f"Coffee for {customer}"

async def main():
    start = time()

    print(f"[{ctime()}] โปรแกรมเริ่มต้น\n")

    # await = หยุดรอที่นี่จนกว่า brew_coffee จะเสร็จ แล้วค่อยได้ผลลัพธ์
    result = await brew_coffee("ลูกค้า A")

    print(f"\nได้ผลลัพธ์: {result}")
    print(f"[{ctime()}] โปรแกรมจบ | ใช้เวลา: {time()-start:.2f}s")

asyncio.run(main())

# สรุป:
# await asyncio.sleep(2)  ≠  time.sleep(2)
# - time.sleep(2)           บล็อก thread ทั้งหมด 2 วินาที
# - await asyncio.sleep(2)  หยุดแค่ coroutine นี้ แต่ event loop ยังรัน coroutine อื่นได้
