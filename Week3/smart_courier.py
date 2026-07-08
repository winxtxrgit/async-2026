# Delivery System): นักศึกษาต้องเขียน try...except CancelledError ได้ถูกต้อง
# และใช้ .get_name(), .cancel(), และ .cancelled() ได้
import asyncio
from time import ctime


async def delivery_task(package_id, duration):
    """จำลองการส่งพัสดุด้วย asyncio.sleep(duration)"""
    try:
        print(f"{ctime()} Courier: Start delivering package {package_id} "
              f"(estimated {duration} sec)...")
        await asyncio.sleep(duration)
        print(f"{ctime()} Courier: Finished delivering package {package_id}.")
        return f"Package {package_id} Delivered!"
    except asyncio.CancelledError:
        # ดักจับการยกเลิกเพื่อทำความสะอาดทรัพยากร แล้วส่งต่อ (re-raise) เพื่อจบการยกเลิก
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise


async def main():
    # สร้าง Task 1 ตัว: package_id="P001", duration=5.0 และตั้งชื่อ "Express-Courier"
    task = asyncio.create_task(
        delivery_task(package_id="P001", duration=5.0),
        name="Express-Courier",
    )

    # จำลองว่าพัสดุกำลังเดินทาง ผ่านไป 2 วินาที
    await asyncio.sleep(2.0)

    # ตรวจสอบสถานะแบบแฝงว่า Task เสร็จหรือยัง และพิมพ์ชื่อ Task ปัจจุบันออกมา
    print(f"{ctime()} Checkpoint: Task '{task.get_name()}' done? {task.done()}")

    # หากผ่านไป 2 วินาทีแล้วยังไม่เสร็จ ให้ยกเลิกงานทันที
    if not task.done():
        print(f"{ctime()} Main: Delivery took too long! Canceling '{task.get_name()}'...")
        task.cancel()

    # รอให้การยกเลิกทำงานจนเสร็จ (จับ CancelledError ที่ถูก re-raise ออกมา)
    try:
        result = await task
        print(f"{ctime()} Main: Result -> {result}")
    except asyncio.CancelledError:
        print(f"{ctime()} Main: The delivery task was cancelled.")

    # ตรวจสอบสถานะตัวแปรภายนอกว่า .cancelled() เป็น True หรือไม่
    print(f"{ctime()} Main: Task cancelled()? {task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
