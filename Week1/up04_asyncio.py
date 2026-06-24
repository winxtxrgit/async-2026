from time import ctime, time
import asyncio

# 1 ลูกค้า = 2 ขั้นต่อเนื่อง: ชงกาแฟ (1 วิ) แล้วอัปเดตจอ LCD (1 วิ)
async def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    await asyncio.sleep(1)  # เวลาชงกาแฟ 1 วินาที (ไม่บล็อก event loop)
    print(f"{ctime()} | Coffee ready for {customer_name}!")

async def update_lcd(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    await asyncio.sleep(1)  # เวลาประมวลผลหน้าจอ LCD 1 วินาที (ไม่บล็อก event loop)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

async def serve_customer(customer_name):
    await make_coffee(customer_name)
    await update_lcd(customer_name)

async def main():
    print(f"{ctime()} | === Asyncio Coffee Machine ===")
    customers = ["A", "B", "C"]

    start = time()

    # asyncio: ทุก task ทำพร้อมกันบน event loop เดียว (รวมเหลือ ~2 วินาที)
    await asyncio.gather(*(serve_customer(c) for c in customers))

    print(f"{ctime()} | Total time: {time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
