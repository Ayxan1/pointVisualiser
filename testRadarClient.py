import asyncio
import websockets
import json
import random
import time

async def send_radar_data():
    uri = "ws://localhost:8765"  # Replace with the WebSocket server URI

    async with websockets.connect(uri) as websocket:
        while True:
            x = random.uniform(0, 800)
            y = random.uniform(0, 800)
            radar_data = {"x": x, "y": y}
            data = json.dumps(radar_data)
            await websocket.send(data)
            print(f"Sent radar data: {radar_data}")
            await asyncio.sleep(1)  # Adjust the sending frequency as needed

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_radar_data())
