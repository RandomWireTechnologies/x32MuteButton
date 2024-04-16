import asyncio
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

async def query_value():
    client = udp_client.SimpleUDPClient("192.168.2.240", 10023)
    while True:
        client.send_message("/ch/8/mix/on", "")
        await asyncio.sleep(1)

async def print_state():
    while True:
        print("Querying /ch/8/mix/on value...")
        await asyncio.sleep(30)

def handle_response(address, *args):
    print(f"Received response from {address}: {args}")

async def main():
    task1 = asyncio.create_task(query_value())
    task2 = asyncio.create_task(print_state())

    dispatch = dispatcher.Dispatcher()
    dispatch.map("/response", handle_response)

    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", 10023), dispatch, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    await asyncio.gather(task1, task2)

    transport.close()

if __name__ == "__main__":
    asyncio.run(main())
