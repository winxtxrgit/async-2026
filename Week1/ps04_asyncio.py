from time import ctime, time, process_time
import asyncio
import os
import threading
import psutil

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name}")
    sum(i * i for i in range(1000000))  # งานคำนวณ CPU-bound เพื่อให้เห็น CPU time จริง
    await asyncio.sleep(2)  # จำลองเวลาชงกาแฟ 2 วินาที (ไม่บล็อก event loop)
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕")

def report_resource(label, wall, cpu):
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / (1024 * 1024)
    print(f"\n----- สรุปทรัพยากร ({label}) -----")
    print(f"เวลาจริง (wall time)   : {wall:.2f} วินาที")
    print(f"เวลา CPU (process_time): {cpu:.2f} วินาที")
    print(f"จำนวน thread ที่ใช้     : {proc.num_threads()}")
    print(f"หน่วยความจำ (RSS)       : {mem:.2f} MB")

async def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    start_wall = time()
    start_cpu = process_time()

    # asyncio: ทุก task รันบน thread เดียว ใช้ทรัพยากรน้อยที่สุด
    await asyncio.gather(*(make_coffee(c) for c in customers))

    wall = time() - start_wall
    cpu = process_time() - start_cpu
    report_resource("asyncio", wall, cpu)

if __name__ == "__main__":
    asyncio.run(main())
