# foodcourt_03_wait_first.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "65010001"
    print(f"{ctime()} | --- [Task 3] Practice using wait (FIRST_COMPLETED) ---")

    start_time = perf_counter()

    # 1. Place 3 racing orders at once (wrap coroutines into Task objects).
    tasks = [
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Thigh")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")),
    ]

    # 2. Wait only until the FIRST order is completed.
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3. Pick up the fastest dish (the winner).
    winner = done.pop()
    result = winner.result()
    print(f"{ctime()} | Winner served dish: Shop: {result['shop']} | Menu: {result['menu']}")

    # 4. Actively clean up: cancel every remaining pending order.
    print(f"{ctime()} | Cleaning up: Canceling {len(pending)} remaining pending orders...")
    for task in pending:
        task.cancel()

    elapsed = perf_counter() - start_time
    print(f"{ctime()} | Total waiting time for the first dish: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
