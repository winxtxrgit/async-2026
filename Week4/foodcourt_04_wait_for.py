# foodcourt_04_wait_for.py
import asyncio
from time import ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "65010001"
    print(f"{ctime()} | --- [Task 4] Practice using wait_for to handle timeouts ---")

    # Steak normally takes 4.0s, but we only have a 2.0s lunch break.
    TIMEOUT_LIMIT = 2.0

    try:
        print(f"{ctime()} | [System] Order sent. Monitoring {TIMEOUT_LIMIT}s timeout limit...")

        # Enforce a hard time ceiling on the network operation.
        result = await asyncio.wait_for(
            send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"),
            timeout=TIMEOUT_LIMIT,
        )

        # This only runs if the steak somehow finishes within the limit.
        print(f"{ctime()} | Steak served in time! Menu: {result['menu']}")

    except asyncio.TimeoutError:
        # Graceful fallback when the backend responds too slowly.
        print(f"{ctime()} | Timeout occurred: Steak took too long! Leaving the food court now.")

if __name__ == "__main__":
    asyncio.run(main())
