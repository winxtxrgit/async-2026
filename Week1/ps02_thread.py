from time import sleep, ctime, time, process_time
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name}")
    sum(i * i for i in range(1000000))  # งานคำนวณ CPU-bound เพื่อให้เห็น CPU time จริง
    sleep(2)  # จำลองเวลาในการชงกาแฟ 2 วินาที
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕")

def report_resource(label, wall, cpu):
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / (1024 * 1024)
    print(f"\n----- สรุปทรัพยากร ({label}) -----")
    print(f"เวลาจริง (wall time)   : {wall:.2f} วินาที")
    print(f"เวลา CPU (process_time): {cpu:.2f} วินาที")
    print(f"จำนวน thread ที่ใช้     : {proc.num_threads()}")
    print(f"หน่วยความจำ (RSS)       : {mem:.2f} MB")

def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    start_wall = time()
    start_cpu = process_time()

    # thread: หลาย thread ใน process เดียว จำนวน thread จึงเพิ่มขึ้น
    threads = [threading.Thread(target=make_coffee, args=(c,)) for c in customers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    wall = time() - start_wall
    cpu = process_time() - start_cpu
    report_resource("thread", wall, cpu)

if __name__ == "__main__":
    main()
