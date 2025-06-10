import asyncio
import websockets
import requests
import json

connected_clients = set()

async def broadcast_iss_location():
    while True:
        try:
            resp = requests.get("http://api.open-notify.org/iss-now.json")
            data = resp.json()
            message = json.dumps({
                "timestamp": data["timestamp"],
                "latitude": data["iss_position"]["latitude"],
                "longitude": data["iss_position"]["longitude"]
            })
            if connected_clients:
                await asyncio.wait([asyncio.create_task(client.send(message)) for client in connected_clients])
        except Exception as e:
            print(f"Error fetching or broadcasting ISS location: {e}")
        await asyncio.sleep(2)

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handler, "0.0.0.0", 8765)
    await asyncio.gather(
        broadcast_iss_location(),
        server.wait_closed()
    )

if __name__ == "__main__":
    asyncio.run(main())