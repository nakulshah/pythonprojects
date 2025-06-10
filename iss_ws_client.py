# iss_ws_client.py
import asyncio
import websockets

async def listen():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to ISS WebSocket server.")
        try:
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(listen())