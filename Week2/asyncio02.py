# Program 2: The Coroutine Object
# Concept: Seeing that calling an async def function creates an "Object" but does not execute it yet.

import inspect

async def say_hello():
    print("สวัสดี! ฉันกำลังรันอยู่ตอนนี้")
    return 42

print("=== ทดสอบว่าการเรียก async function ไม่ได้รันทันที ===\n")

print("ก่อนเรียก say_hello()")
coro = say_hello()   # <-- เรียกฟังก์ชัน แต่ยังไม่รัน!
print("หลังเรียก say_hello()\n")

print(f"type(coro)           : {type(coro)}")
print(f"inspect.iscoroutine? : {inspect.iscoroutine(coro)}")
print()
print("สังเกต: 'สวัสดี! ฉันกำลังรันอยู่ตอนนี้' ยังไม่ถูกพิมพ์เลย!")
print("เพราะ coroutine ต้องถูก await หรือส่งให้ event loop ก่อนถึงจะรัน")

# ปิด coroutine เพื่อหลีกเลี่ยง RuntimeWarning
coro.close()
print("\n(coroutine ถูกปิดแล้วโดยไม่ได้รันเลย)")
