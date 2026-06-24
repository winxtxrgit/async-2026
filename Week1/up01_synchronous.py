from time import sleep, ctime, time

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
    print(f"{ctime()} | === Synchronous Coffee Machine ===")
    customers = ["A", "B", "C"]

    start = time()

    # synchronous: บริการทีละคนจนครบ (รวม 3 คน x 2 วิ = 6 วินาที)
    for customer in customers:
        serve_customer(customer)

    print(f"{ctime()} | Total time: {time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
