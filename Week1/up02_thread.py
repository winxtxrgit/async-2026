from time import sleep, ctime, time
import threading

# 1 ลูกค้า = 2 ขั้นต่อเนื่อง: ชงกาแฟ (1 วิ) แล้วอัปเดตจอ LCD (1 วิ)
def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1)  # เวลาชงกาแฟ 1 วินาที
    print(f"{ctime()} | Coffee ready for {customer_name}!")

def update_lcd(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1)  # เวลาประมวลผลหน้าจอ LCD 1 วินาที
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def serve_customer(customer_name):
    make_coffee(customer_name)
    update_lcd(customer_name)

def main():
    print(f"{ctime()} | === Multi-threading Coffee Machine ===")
    customers = ["A", "B", "C"]

    start = time()

    # thread: บริการทุกคนพร้อมกัน 1 thread ต่อ 1 คน (รวมเหลือ ~2 วินาที)
    threads = [threading.Thread(target=serve_customer, args=(c,)) for c in customers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"{ctime()} | Total time: {time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
