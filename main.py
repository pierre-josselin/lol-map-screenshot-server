import dotenv
import http.server
import io
import os
import mss
import socketserver

from PIL import Image

dotenv.load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
MONITOR_INDEX = int(os.getenv("MONITOR_INDEX"))
MAP_WIDTH = int(os.getenv("MAP_WIDTH"))
MAP_HEIGHT = int(os.getenv("MAP_HEIGHT"))

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        image = sct.grab(bbox)
        image = Image.frombytes("RGB", image.size, image.bgra, "raw", "BGRX")

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.send_header("Content-length", str(len(image_bytes)))
        self.end_headers()
        self.wfile.write(image_bytes)

if __name__ == "__main__":
    sct = mss.mss()
    monitor = sct.monitors[MONITOR_INDEX]

    bbox = {
        "top": monitor["height"] - MAP_HEIGHT,
        "left": monitor["width"] - MAP_WIDTH,
        "width": MAP_WIDTH,
        "height": MAP_HEIGHT,
    }

    with socketserver.TCPServer((HOST, PORT), HTTPRequestHandler) as httpd:
        httpd.serve_forever()
