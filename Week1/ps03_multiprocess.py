from time import sleep, ctime, time, process_time
import multiprocessing
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
# แต่ละ process วัดหน่วยความจำของตัวเองแล้วส่งกลับผ่าน result_queue
def make_coffee(customer_name, result_queue):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name} | PID={os.getpid()}")
    sum(i * i for i in range(1000000))  # งานคำนวณ CPU-bound เพื่อให้เห็น CPU time จริง
    sleep(2)  # จำลองเวลาในการชงกาแฟ 2 วินาที
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕ | PID={os.getpid()}")

    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / (1024 * 1024)
    result_queue.put((customer_name, os.getpid(), mem))

def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    result_queue = multiprocessing.Queue()

    start_wall = time()
    start_cpu = process_time()

    # multiprocess: แต่ละลูกค้าเป็นคนละ process มีหน่วยความจำของตัวเอง
    processes = [
        multiprocessing.Process(target=make_coffee, args=(c, result_queue))
        for c in customers
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    wall = time() - start_wall
    cpu = process_time() - start_cpu

    # รวบรวมผลจากทุก process
    results = [result_queue.get() for _ in customers]

    print(f"\n----- สรุปทรัพยากร (multiprocess) -----")
    print(f"เวลาจริง (wall time)           : {wall:.2f} วินาที")
    print(f"เวลา CPU ของ process หลัก      : {cpu:.2f} วินาที")
    total_mem = 0
    for name, pid, mem in results:
        print(f"  - {name} | PID={pid} | RSS={mem:.2f} MB")
        total_mem += mem
    print(f"หน่วยความจำรวมของทุก process    : {total_mem:.2f} MB")

if __name__ == "__main__":
    main()
