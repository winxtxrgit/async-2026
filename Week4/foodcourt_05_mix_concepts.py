# foodcourt_05_mix_concepts.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "65010001"
    print(f"{ctime()} | --- [Task 5] Advanced Practice: Mixing concepts together ---")

    start_time = perf_counter()

    # 1. Noodle order runs with a standard waiting cycle (1.5s).
    noodle_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
    )

    # 2. Chicken rice order (0.8s) is wrapped under a strict 1.0s timeout,
    #    nesting wait_for directly inside a create_task execution tree.
    chicken_task = asyncio.create_task(
        asyncio.wait_for(
            send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"),
            timeout=1.0,
        )
    )

    try:
        # 3. Resolve both structures inside a single gather() collection.
        results = await asyncio.gather(noodle_task, chicken_task)

        elapsed = perf_counter() - start_time
        print(f"{ctime()} | Success: All food served on time! Received {len(results)} dishes.")
        print(f"{ctime()} | Total elapsed time: {elapsed:.2f} seconds.")

    except asyncio.TimeoutError:
        elapsed = perf_counter() - start_time
        print(f"{ctime()} | Failed: A dish exceeded its timeout limit! Order incomplete.")
        print(f"{ctime()} | Total elapsed time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
