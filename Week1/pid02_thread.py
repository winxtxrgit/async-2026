from time import sleep, ctime, time
import threading
import os

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name} "
          f"| PID={os.getpid()} | Thread={threading.current_thread().name}")
    sleep(2)  # จำลองเวลาในการชงกาแฟ 2 วินาที
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕ | PID={os.getpid()}")

def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]
    print(f"โปรแกรมหลักทำงานที่ PID={os.getpid()}\n")

    start = time()

    # thread: ทุกคนใช้ PID เดียวกัน แต่คนละ Thread (ทำงานพร้อมกัน)
    threads = [threading.Thread(target=make_coffee, args=(c,)) for c in customers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    end = time()
    print(f"\nเสร็จทั้งหมด {len(customers)} คน | ใช้เวลา {end - start:.2f} วินาที")

if __name__ == "__main__":
    main()
