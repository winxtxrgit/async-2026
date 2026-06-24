from time import sleep, ctime, time
import multiprocessing

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"[{ctime()}] เริ่มทำกาแฟให้ {customer_name}")
    sleep(2)  # จำลองเวลาในการชงกาแฟ 2 วินาที
    print(f"[{ctime()}] กาแฟของ {customer_name} เสร็จแล้ว ☕")

def main():
    # คิวลูกค้า
    customers = ["ลูกค้า A", "ลูกค้า B", "ลูกค้า C", "ลูกค้า D"]

    start = time()

    # ทำงานแบบ multi-process: สร้าง 1 process ต่อลูกค้า 1 คน แล้วเริ่มพร้อมกัน
    processes = []
    for customer in customers:
        p = multiprocessing.Process(target=make_coffee, args=(customer,))
        processes.append(p)
        p.start()

    # รอให้ทุก process ทำงานเสร็จก่อนสรุปผล
    for p in processes:
        p.join()

    end = time()
    print(f"\nทำกาแฟให้ลูกค้าทั้งหมด {len(customers)} คน เสร็จสิ้น")
    print(f"ใช้เวลารวมทั้งหมด {end - start:.2f} วินาที")

# สิ่งสำคัญที่สุดสำหรับ Multi-processing ใน Python: ต้องครอบด้วยบล็อกนี้เสมอ
if __name__ == "__main__":
    main()
