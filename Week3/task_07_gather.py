# Objective: Group multiple operations to run concurrently and return an ordered list of outputs.
import asyncio
from time import time, ctime

async def fetch_db_record(table_name, latency):
    await asyncio.sleep(latency)
    return f"RowData_{table_name}"

async def main():
    start = time()

    # gather() รันทุก coroutine พร้อมกัน และคืน list ผลลัพธ์ "ตามลำดับ input" (ไม่ใช่ลำดับที่เสร็จ)
    results = await asyncio.gather(
        fetch_db_record("Users", 1.0),
        fetch_db_record("Products", 0.5),
        fetch_db_record("Invoices", 1.0)
    )

    print(f"{ctime()} Aggregated Output Results List: {results}")
    # รันพร้อมกัน จึงใช้เวลา ~1.0s (ตัวที่ช้าสุด) ไม่ใช่ 2.5s (ผลรวม)
    print(f"{ctime()} Execution Completed in: {time() - start:.2f} seconds")

asyncio.run(main())
