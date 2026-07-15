# foodcourt_02_gather.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "65010001"
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")

    start_time = perf_counter()

    # 1. Create 3 tasks ordering from different shops at the same time.
    tasks = [
        send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"),
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles"),
        send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"),
    ]

    # 2. Run them concurrently and wait for ALL dishes to be completed.
    results = await asyncio.gather(*tasks)

    # 3. Serve every finished dish together.
    for result in results:
        print(f"{ctime()} | [Pickup] Shop: {result['shop']} | Menu: {result['menu']} is ready!")

    # 4. Total time equals the slowest dish (Steak: 4.0s), not the sum of all.
    elapsed = perf_counter() - start_time
    print(f"{ctime()} | Total time: {elapsed:.2f} seconds (Equals to the slowest dish).")

if __name__ == "__main__":
    asyncio.run(main())
