from time import ctime, time
import asyncio

# ========================================================
# Restaurant Simulation — Version 4: Asyncio
# Greeting ทีละคน (Sequential) แล้วสร้าง Async Task ต่อ 1 ลูกค้า
# 3 Tasks รัน 3 ขั้นตอนที่เหลือพร้อมกันบน Single Thread
# ========================================================

STEP_DELAY = 1  # แต่ละขั้นตอนใช้เวลา 1 วินาที

async def greet_customer(customer):
    print(f"[{ctime()}] Greeting for {customer} ...")
    await asyncio.sleep(STEP_DELAY)
    print(f"[{ctime()}] Greeting for {customer} ...Done!")

async def customer_workflow(task_name):
    """ขั้นตอนที่เหลือหลัง Greeting: รันเป็น Async Task"""
    print(f"[{ctime()}]    [{task_name}] Taking Order ...")
    await asyncio.sleep(STEP_DELAY)
    print(f"[{ctime()}]    [{task_name}] Taking Order ...Done!")

    print(f"[{ctime()}]    [{task_name}] Cooking Spaghetti ...")
    await asyncio.sleep(STEP_DELAY)
    print(f"[{ctime()}]    [{task_name}] Cooking Spaghetti ...Done!")

    print(f"[{ctime()}]    [{task_name}] Manage Bar for Drink ...")
    await asyncio.sleep(STEP_DELAY)
    print(f"[{ctime()}]    [{task_name}] Manage Bar for Drink ...Done!")
    print(f"[{ctime()}]    [{task_name}] All served!\n")

async def main():
    customers = ["Customer-A", "Customer-B", "Customer-C"]
    start = time()

    # ขั้นที่ 1: Greeting ทีละคน (Sequential await)
    for customer in customers:
        await greet_customer(customer)

    print(f"\n[{ctime()}] --- All customers greeted. Scheduling independent Async Tasks! ---\n")

    # ขั้นที่ 2: สร้าง Task ต่อ 1 ลูกค้า แล้วรันพร้อมกัน (Concurrent)
    tasks = []
    for customer in customers:
        task_name = f"Task-{customer.split('-')[-1]}"
        task = asyncio.create_task(customer_workflow(task_name))
        tasks.append(task)

    # รอทุก Task เสร็จ
    for task in tasks:
        await task

    elapsed = time() - start
    print(f"[{ctime()}] Finished Entire Restaurant Operation in {elapsed:.2f} seconds.")
    print(f"\n[หมายเหตุ] Asyncio: 3s (greeting) + 3s (concurrent tasks) ≈ 6s | Single Thread!")

if __name__ == "__main__":
    asyncio.run(main())
