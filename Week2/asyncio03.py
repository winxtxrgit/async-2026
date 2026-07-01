# Program 3: The Event Loop (asyncio.run)
# Concept: Using the Event Loop to actually execute a Coroutine Object.

import asyncio

async def say_hello():
    print("สวัสดี! ฉันกำลังรันอยู่ใน Event Loop แล้ว")
    return 42

async def main():
    print("main() เริ่มต้น")

    # await = หยุดรอให้ coroutine นี้เสร็จก่อน แล้วค่อยทำต่อ
    result = await say_hello()

    print(f"ได้ผลลัพธ์จาก say_hello(): {result}")
    print("main() จบแล้ว")

print("ก่อน asyncio.run()")
asyncio.run(main())   # <-- เปิด Event Loop แล้วส่ง main() ให้รัน
print("หลัง asyncio.run()")

# สรุป:
# asyncio.run()  = เปิด Event Loop + รัน coroutine ที่ระบุ + ปิด Event Loop
# await          = หยุดรอ coroutine นั้นเสร็จก่อน (ใช้ได้แค่ใน async def เท่านั้น)
