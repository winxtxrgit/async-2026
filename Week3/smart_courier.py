# Objective: Assignment 1 - The Smart Courier System
# ระบบส่งพัสดุด่วน: ฝึกการควบคุม Task และจัดการ CancelledError
import asyncio
from time import ctime

async def delivery_task(package_id, duration):
    try:
        # พิมพ์ข้อความเริ่มงานส่งของ
        print(f"{ctime()} Courier started delivering {package_id}...")
        
        # จำลองการเดินทางของรถส่งของ
        await asyncio.sleep(duration)
        
        return f"Package {package_id} Delivered!"
        
    except asyncio.CancelledError:
        # พิมพ์ข้อความเมื่อโดนสั่งขอยกเลิกงานตามสเปกเป๊ะๆ
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        # โยนข้อผิดพลาดขึ้นไปเพื่อให้ภายนอกรับรู้
        raise

async def main():
    # สร้าง Task ส่งของและตั้งชื่อเป็น Express-Courier
    task = asyncio.create_task(delivery_task("P001", 5.0), name="Express-Courier")
    
    # ปล่อยให้พนักงานส่งของวิ่งไป 2 วินาทีแรก
    await asyncio.sleep(2.0)
    
    # พิมพ์เช็กสถานะการทำงาน
    print(f"{ctime()} Checking task '{task.get_name()}'. Is it done? {task.done()}")
    
    # หากพบว่าส่งช้าเกินกำหนด (ยังไม่ done) ให้ยกเลิกทันที
    if not task.done():
        print(f"{ctime()} Taking too long! Canceling the task...")
        task.cancel()
        
    # รอเคลียร์ผลลัพธ์สุดท้าย
    try:
        await task
    except asyncio.CancelledError:
        pass
        
    # พิมพ์ยืนยันสถานะความสำเร็จในข่ายยกเลิก
    print(f"{ctime()} Final verify: Is task officially canceled? {task.cancelled()}")

if __name__ == "__main__":
    asyncio.run(main())
