# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.

import inspect

# ฟังก์ชันปกติ (Normal Function)
def normal_function():
    return "Hello from normal function"

# Async function (Coroutine Function)
async def coroutine_function():
    return "Hello from coroutine function"

print("--- ทดสอบ normal function ---")
print(f"type(normal_function)  : {type(normal_function)}")
print(f"iscoroutinefunction?   : {inspect.iscoroutinefunction(normal_function)}")
result = normal_function()
print(f"ผลลัพธ์เมื่อเรียก       : {result}")

print()
print("--- ทดสอบ async def function ---")
print(f"type(coroutine_function)  : {type(coroutine_function)}")
print(f"iscoroutinefunction?      : {inspect.iscoroutinefunction(coroutine_function)}")

# สังเกต: เรียก coroutine_function() ได้ แต่ยังไม่รัน! ได้แค่ Object
coro = coroutine_function()
print(f"\nเมื่อเรียก coroutine_function():")
print(f"  type(coro)         : {type(coro)}")
print(f"  iscoroutine(coro)? : {inspect.iscoroutine(coro)}")
print(f"  สังเกต: ยังไม่ได้พิมพ์อะไรออกมาเลย! (ยังไม่ได้รัน)")

coro.close()  # ปิด coroutine ที่ยังไม่ได้ await เพื่อไม่ให้เกิด warning
