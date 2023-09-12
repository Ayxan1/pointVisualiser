import cv2
import asyncio
import websockets
import json
import numpy as np

# Create a black background canvas
canvas_size = (800, 800)  # Adjust the size as needed
background_color = (0, 0, 0)
canvas = np.zeros((canvas_size[0], canvas_size[1], 3), dtype=np.uint8)
canvas[:] = background_color

# Function to visualize radar data and clear old data
def visualize_radar_data(data):
    global canvas
    # Clear the canvas by filling it with the background color
    canvas[:] = background_color

    # Assuming data is in the format: {"x": x_value, "y": y_value}
    x = int(data["x"])
    y = int(data["y"])
    
    # Draw a red circle at the specified (x, y) coordinates
    cv2.circle(canvas, (x, y), 5, (0, 0, 255), -1)

async def radar_data_handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
            radar_data = json.loads(data)
            visualize_radar_data(radar_data)
            cv2.imshow('Radar Data Visualization', canvas)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except websockets.ConnectionClosed:
            break

if __name__ == "__main__":
    start_server = websockets.serve(radar_data_handler, "localhost", 8765)

    # Initialize OpenCV window
    cv2.namedWindow('Radar Data Visualization', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Radar Data Visualization', canvas_size[0], canvas_size[1])

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
