import uvicorn
import os
import cv2 as cv
import threading

from pydantic import BaseModel
import numpy as np

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import time
from gpio import *
app = FastAPI()


class ExtParams(BaseModel):
    name: str
    length: int


CHUNK_SIZE = 1024 * 1024


base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = base_path+"\\video"
if not os.path.exists(base_path):
    os.makedirs(base_path)

fourcc = cv.VideoWriter_fourcc(*'XVID')
fourcc_h264 = cv.VideoWriter_fourcc(*'H264')
fourcc_mjpg = cv.VideoWriter_fourcc(*'MJPG')
fourcc_yuv2 = cv.VideoWriter_fourcc(*'YUV2')

record = False

# v4l2-ctl -d 0 --list-formats # dev/video0
# v4l2-ctl -d 0 --list-formats-ext # dev/video0


STREAM_WIDTH = 640 
STREAM_HEIGHT = 480

global cam_1
global cam_2

CAM_1_ID = 0
CAM_2_ID = 2

cam_1 = cv.VideoCapture(CAM_1_ID)
cam_2 = cv.VideoCapture(CAM_2_ID)

cam_1.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_1.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_1.set(cv.CAP_PROP_FPS, 15)
cam_1.set(cv.CAP_PROP_FOURCC, fourcc_yuv2)
cam_1.set(cv.CAP_PROP_BUFFERSIZE, 5)

cam_2.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_2.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_2.set(cv.CAP_PROP_FPS, 15)
cam_2.set(cv.CAP_PROP_FOURCC, fourcc_yuv2)
cam_2.set(cv.CAP_PROP_BUFFERSIZE, 5)


def frame_to_byte(frame):
    # print('disconnected during stream')

    ret, buffer = cv.imencode('.jpg', frame)
    # frame을 byte로 변경 후 특정 식??으로 변환 후에
    # yield로 하나씩 넘겨준다.
    return buffer.tobytes()

async def read_cam(cam_id=0):
    global cam_1
    global cam_2

    if cam_id == CAM_1_ID:
        while True:
            # camera 정의
            # cam = cv.VideoCapture(cam_id, cv.CAP_DSHOW) # Windows의 경우 이걸 실행
            print(cam_1.get(cv.CAP_PROP_FPS), flush=True)

            if cam_1.isOpened():
                while True:
                    # 카메라 값 불러오기
                    await asyncio.sleep(0.06)
                    ret, frame = cam_1.read()

                    # frame = frame.astype(np.uint8)

                    # frame = cv.resize(frame,(480,640))
                    if ret:
                        yield (b'--frame\r\n'
                            b'Content-Type:image/jpeg\r\n'
                            b'Content-Length: ' + f"{len(frame_to_byte(frame))}".encode() + b'\r\n'
                            b'\r\n' + bytearray(frame_to_byte(frame)) + b'\r\n')
                        
                    else:
                        # # await reconnect_cam()
                        # print('[WARN @ {}]cannot read frame from cam_1.. releasing...'.format(time.time()))
                        # cam_1.release()
                        


                        loading_img = cv.imread('./assets/cam1_opening.png')

                        yield (b'--frame\r\n'
                            b'Content-Type:image/jpeg\r\n'
                            b'Content-Length: ' + f"{len(frame_to_byte(loading_img))}".encode() + b'\r\n'
                            b'\r\n' + bytearray(frame_to_byte(loading_img)) + b'\r\n')
                        await asyncio.sleep(1)

                        break

            else:
                while True:
                    cam_1.release()
                    print('[WARN @ {}]cam_is not opened.. trying to reconnect'.format(time.time()))
                    cam_1=cv.VideoCapture(cam_id)
                    cam_1.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
                    cam_1.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
                    cam_1.set(cv.CAP_PROP_FPS, 15)
                    cam_1.set(cv.CAP_PROP_FOURCC, fourcc_yuv2)
                    cam_1.set(cv.CAP_PROP_BUFFERSIZE, 5)
                    
                    if cam_1.isOpened():
                        break

                    loading_img = cv.imread('./assets/cam1_opening.png')

                    yield (b'--frame\r\n'
                        b'Content-Type:image/jpeg\r\n'
                        b'Content-Length: ' + f"{len(frame_to_byte(loading_img))}".encode() + b'\r\n'
                        b'\r\n' + bytearray(frame_to_byte(loading_img)) + b'\r\n')

                    await asyncio.sleep(1)
            await asyncio.sleep(1)



        # print('[WARN @ {}]cam_is terminated outside of while scope'.format(time()))
    if cam_id == CAM_2_ID:
        while True:
            # camera 정의
            # cam = cv.VideoCapture(cam_id, cv.CAP_DSHOW) # Windows의 경우 이걸 실행
            print(cam_2.get(cv.CAP_PROP_FPS), flush=True)
            await asyncio.sleep(0.06)

            if cam_2.isOpened():
                while True:
                    # 카메라 값 불러오기
                    ret, frame = cam_2.read()
                    # frame = frame.astype(np.uint8)
                    # frame = cv.resize(frame,(480,640))

                    if ret:
                        yield (b'--frame\r\n'
                            b'Content-Type:image/jpeg\r\n'
                            b'Content-Length: ' + f"{len(frame_to_byte(frame))}".encode() + b'\r\n'
                            b'\r\n' + bytearray(frame_to_byte(frame)) + b'\r\n')
                        
                    else:
                        # # await reconnect_cam()
                        # print('[WARN @ {}]cannot read frame from cam_2.. releasing...'.format(time.time()))
                        # cam_2.release()


                        loading_img = cv.imread('./assets/cam1_opening.png')

                        yield (b'--frame\r\n'
                            b'Content-Type:image/jpeg\r\n'
                            b'Content-Length: ' + f"{len(frame_to_byte(loading_img))}".encode() + b'\r\n'
                            b'\r\n' + bytearray(frame_to_byte(loading_img)) + b'\r\n')

                        break

            else:
                while True:
                    cam_2.release()
                    print('[WARN @ {}]cam2_is not opened.. trying to reconnect'.format(time.time()))
                    cam_2=cv.VideoCapture(cam_id)
                    cam_2.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
                    cam_2.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
                    cam_2.set(cv.CAP_PROP_FPS, 15)
                    cam_2.set(cv.CAP_PROP_FOURCC, fourcc_yuv2)
                    cam_2.set(cv.CAP_PROP_BUFFERSIZE, 5)
                    
                    if cam_2.isOpened():
                        break
                    
                    loading_img = cv.imread('./assets/cam1_opening.png')

                    yield (b'--frame\r\n'
                        b'Content-Type:image/jpeg\r\n'
                        b'Content-Length: ' + f"{len(frame_to_byte(loading_img))}".encode() + b'\r\n'
                        b'\r\n' + bytearray(frame_to_byte(loading_img)) + b'\r\n')
            await asyncio.sleep(1)

        print('[WARN @ {}]cam2_is terminated outside of while scope'.format(time.time()))

        
@app.get("/1")
async def bird_detection():
    
    return StreamingResponse(read_cam(cam_id=CAM_1_ID), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/2")
async def bird_detection_2():
    return StreamingResponse(read_cam(cam_id=CAM_2_ID), media_type="multipart/x-mixed-replace; boundary=frame")


@app.post("/cmd/ext")
# EXTERMINATION
async def extermination(item: ExtParams):

    # exec_ext(interval=item.length)
    t = threading.Thread(target=exec_ext, args=(item.length,))
    t.start()
    return {"length": item.length, "code": 200}


if __name__ == "__main__":
    init_gpio()
    uvicorn.run(app, host="0.0.0.0", port=5000)
