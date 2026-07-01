from time import sleep, ctime, time
import multiprocessing

# ========================================================
# Restaurant Simulation — Version 3: Multi-Processing
# สร้าง Process ต่อ 1 ลูกค้า แต่ละ Process รัน ALL 4 ขั้นตอน
# พร้อมกันอย่างแท้จริง (True Parallelism) บน CPU หลายแกน
# ========================================================

STEP_DELAY = 1

def serve_customer(customer):
    """รัน 4 ขั้นตอนครบทั้งหมดสำหรับลูกค้า 1 คน — ใน Process แยก"""
    print(f"[{ctime()}] Greeting for {customer} ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] Greeting for {customer} ...Done!")

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

    print(f"[{ctime()}] --- Starting {len(customers)} independent Processes! ---\n")

    # สร้าง Process ต่อ 1 ลูกค้า (True Parallelism — ไม่มี GIL ขวาง)
    processes = []
    for customer in customers:
        p = multiprocessing.Process(target=serve_customer, args=(customer,))
        processes.append(p)
        p.start()

    # รอทุก Process ทำงานเสร็จ
    for p in processes:
        p.join()

    elapsed = time() - start
    print(f"[{ctime()}] Finished Entire Restaurant Operation in {elapsed:.2f} seconds.")
    print(f"\n[หมายเหตุ] Multiprocessing: 3 processes รันพร้อมกัน 4 ขั้นตอน ≈ 4s (เร็วที่สุด)")

# สำคัญมาก: Multi-processing ใน Python ต้องครอบด้วย if __name__ == "__main__" เสมอ
if __name__ == "__main__":
    main()
