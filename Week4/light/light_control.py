# light_control.py
# 💡 Smart Lab Lighting - Controller (2 modes)
#   Mode 1: ไฟติดเรียง (Sequential)  -> เปิดทีละดวง รอดวงก่อนหน้าเสร็จก่อน
#   Mode 2: ไฟติดแบบ async (Concurrent) -> สั่งเปิดทุกดวงพร้อมกันด้วย asyncio.gather
#
# ต้องรัน server ก่อน: uvicorn light_api:app --port 8000

import asyncio
from time import ctime, perf_counter

import httpx

BASE_URL = "http://172.16.2.117:8088"
MY_STUDENT_ID = "6710301032"
LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


async def set_light(student_id: str, light_id: str, status: str) -> dict:
    """สั่งเปิด/ปิดไฟ 1 ดวงผ่าน HTTP API (server จะหน่วงตาม hardware delay ของดวงนั้น)."""
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"status": status}, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                print(f"{ctime()} | [OK] {light_id} -> {data['current_status']}")
                return data
            return {"status": "ERROR", "detail": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}


async def mode_sequential(status: str = "ON"):
    """โหมด 1: ไฟติดเรียง — เปิดทีละดวง (เวลารวม = ผลบวกของทุก delay)."""
    print(f"\n{ctime()} | === Mode 1: ไฟติดเรียง (Sequential) ===")
    start = perf_counter()

    for light_id in LIGHTS:
        await set_light(MY_STUDENT_ID, light_id, status)

    elapsed = perf_counter() - start
    print(f"{ctime()} | รวมเวลา (เรียง): {elapsed:.2f} วินาที (= ผลบวกของทุก delay)")


async def mode_async(status: str = "ON"):
    """โหมด 2: ไฟติดแบบ async — สั่งทุกดวงพร้อมกัน (เวลารวม = ดวงที่ช้าสุด)."""
    print(f"\n{ctime()} | === Mode 2: ไฟติดแบบ async (Concurrent) ===")
    start = perf_counter()

    tasks = [set_light(MY_STUDENT_ID, light_id, status) for light_id in LIGHTS]
    await asyncio.gather(*tasks)

    elapsed = perf_counter() - start
    print(f"{ctime()} | รวมเวลา (async): {elapsed:.2f} วินาที (= ดวงที่ช้าที่สุด)")


async def reset():
    """ปิดไฟทุกดวงกลับเป็น OFF ก่อนเริ่มรอบใหม่."""
    async with httpx.AsyncClient() as client:
        await client.delete(f"{BASE_URL}/api/{MY_STUDENT_ID}/lights/reset", timeout=10.0)


async def main():
    print("💡 Smart Lab Lighting Controller")
    print("  1) ไฟติดเรียง (Sequential)")
    print("  2) ไฟติดแบบ async (Concurrent)")
    print("  3) เทียบทั้ง 2 โหมด")
    choice = input("เลือกโหมด (1/2/3): ").strip()

    if choice == "1":
        await reset()
        await mode_sequential("ON")
    elif choice == "2":
        await reset()
        await mode_async("ON")
    elif choice == "3":
        await reset()
        await mode_sequential("ON")
        await reset()
        await mode_async("ON")
    else:
        print("ไม่มีโหมดนี้")


if __name__ == "__main__":
    asyncio.run(main())
