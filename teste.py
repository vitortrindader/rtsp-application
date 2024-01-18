import cv2
import subprocess

width, height = 640, 480
fps = 30
rtsp_url = "rtsp://localhost:8554/mystream"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, fps)

ffmpeg_cmd = [
    "ffmpeg",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-s", f"{width}x{height}",
    "-r", str(fps),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "ultrafast",
    "-f", "rtsp",
    "-rtsp_transport", "tcp",
    rtsp_url
]

ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

while True:
    ret, frame = cap.read()
    ffmpeg_process.stdin.write(frame.tobytes())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()
