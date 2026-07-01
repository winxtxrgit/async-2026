from time import sleep, ctime, time
import threading

# ========================================================
# Restaurant Simulation — Version 2: Multi-Threading
# Greeting ทีละคน (Sequential) แล้วสร้าง Thread ต่อ 1 ลูกค้า
# แต่ละ Thread รัน 3 ขั้นตอนที่เหลือพร้อมกัน
# ========================================================

STEP_DELAY = 1

def greet_customer(customer):
    print(f"[{ctime()}] Greeting for {customer} ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] Greeting for {customer} ...Done!")

def customer_workflow(customer):
    """ขั้นตอนที่เหลือหลัง Greeting: รันใน Thread แยก"""
    print(f"[{ctime()}] [{customer}] Taking Order ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Taking Order ...Done!")

    print(f"[{ctime()}] [{customer}] Cooking Spaghetti ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Cooking Spaghetti ...Done!")

    print(f"[{ctime()}] [{customer}] Manage Bar for Drink ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Manage Bar for Drink ...Done!")
    print(f"[{ctime()}] [{customer}] All served!\n")

def main():
    customers = ["Customer-A", "Customer-B", "Customer-C"]
    start = time()

    # ขั้นที่ 1: Greeting ทีละคน (Sequential)
    for customer in customers:
        greet_customer(customer)

    print(f"\n[{ctime()}] --- All customers greeted. Scheduling independent Threads! ---\n")

    # ขั้นที่ 2: สร้าง Thread ต่อ 1 ลูกค้า แล้ว start พร้อมกัน
    threads = []
    for customer in customers:
        t = threading.Thread(target=customer_workflow, args=(customer,))
        threads.append(t)
        t.start()

    # รอทุก Thread ทำงานเสร็จ
    for t in threads:
        t.join()

    elapsed = time() - start
    print(f"[{ctime()}] Finished Entire Restaurant Operation in {elapsed:.2f} seconds.")
    print(f"\n[หมายเหตุ] Threading: 3s (greeting) + 3s (concurrent threads) ≈ 6s")

if __name__ == "__main__":
    main()
