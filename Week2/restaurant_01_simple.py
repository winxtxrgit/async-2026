from time import sleep, ctime, time

# ========================================================
# Restaurant Simulation — Version 1: Synchronous (Simple)
# ทำงานทีละขั้นตอน ทีละลูกค้า ไม่มีการทำงานพร้อมกันเลย
# ========================================================

STEP_DELAY = 1  # แต่ละขั้นตอนใช้เวลา 1 วินาที

def greet_customer(customer):
    print(f"[{ctime()}] Greeting for {customer} ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] Greeting for {customer} ...Done!")

def take_order(customer):
    print(f"[{ctime()}] [{customer}] Taking Order ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Taking Order ...Done!")

def cook(customer):
    print(f"[{ctime()}] [{customer}] Cooking Spaghetti ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Cooking Spaghetti ...Done!")

def manage_bar(customer):
    print(f"[{ctime()}] [{customer}] Manage Bar for Drink ...")
    sleep(STEP_DELAY)
    print(f"[{ctime()}] [{customer}] Manage Bar for Drink ...Done!")
    print(f"[{ctime()}] [{customer}] All served!\n")

def serve_customer(customer):
    greet_customer(customer)
    take_order(customer)
    cook(customer)
    manage_bar(customer)

def main():
    customers = ["Customer-A", "Customer-B", "Customer-C"]
    start = time()

    # ทำงาน Sequential: ลูกค้า A จบทุกขั้นตอนก่อน แล้วค่อยไปลูกค้า B, C
    for customer in customers:
        serve_customer(customer)

    elapsed = time() - start
    print(f"[{ctime()}] Finished Entire Restaurant Operation in {elapsed:.2f} seconds.")
    print(f"\n[หมายเหตุ] Synchronous: {len(customers)} customers × 4 steps × {STEP_DELAY}s = ~{len(customers)*4*STEP_DELAY}s")

if __name__ == "__main__":
    main()
