from time import sleep, ctime, time
import threading

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name}")
    sleep(2)  # จำลองเวลาในการชงกาแฟ 2 วินาที
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕")

def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    start = time()

    # ทำงานแบบ thread: สร้าง 1 thread ต่อลูกค้า 1 คน แล้วเริ่มพร้อมกัน
    threads = []
    for customer in customers:
        t = threading.Thread(target=make_coffee, args=(customer,))
        threads.append(t)
        t.start()

    # รอให้ทุก thread ทำงานเสร็จก่อนสรุปผล
    for t in threads:
        t.join()

    end = time()
    print(f"\nทำกาแฟให้ลูกค้าทั้งหมด {len(customers)} คน เสร็จสิ้น")
    print(f"ใช้เวลารวมทั้งหมด {end - start:.2f} วินาที")

# สั่งให้โปรแกรมทำงาน
if __name__ == "__main__":
    main()
