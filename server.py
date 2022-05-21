import uvicorn, os
import cv2 as cv
import threading

from fastapi import FastAPI
# from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

from gpio import *
app = FastAPI()


# templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024 * 1024


base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = base_path+"\\video"
if not os.path.exists(base_path):
    os.makedirs(base_path)

fourcc = cv.VideoWriter_fourcc(*'XVID')
record = False

STREAM_WIDTH = 480
STREAM_HEIGHT = 270

cam_1 = cv.VideoCapture(0)
cam_2 = cv.VideoCapture(2)
cam_3 = cv.VideoCapture(4)
cam_4 = cv.VideoCapture(6)

cam_1.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_1.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_1.set(cv.CAP_PROP_FPS, 15)
# cap.set(cv.CAP_PROP_FOURCC, cv.FOURCC('M', 'J', 'P', 'G'));

cam_2.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_2.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_2.set(cv.CAP_PROP_FPS, 15)

cam_3.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_3.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_3.set(cv.CAP_PROP_FPS, 15)

cam_4.set(cv.CAP_PROP_FRAME_WIDTH, STREAM_WIDTH)
cam_4.set(cv.CAP_PROP_FRAME_HEIGHT, STREAM_HEIGHT)
cam_4.set(cv.CAP_PROP_FPS, 15)

def read_cam(cam, cam_id=0):

    # camera 정의
    # cam = cv.VideoCapture(cam_id, cv.CAP_DSHOW) # Windows의 경우 이걸 실행

    if not cam.isOpened():
        if cam_id == 0:
            loading_img = cv.imread('./assets/cam1_opening.png')
        elif cam_id == 1:
            loading_img = cv.imread('./assets/cam2_opening.png')
        elif cam_id == 2:
            loading_img = cv.imread('./assets/cam3_opening.png')
        else:
            loading_img = cv.imread('./assets/cam3_opening.png')

        ret, img = cv.imencode('.jpg', loading_img)

        byte_img = img.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(byte_img) + b'\r\n')

    while cam.isOpened():
        # 카메라 값 불러오기
        success, frame = cam.read()

        if not success:

            if cam_id == 0:
                loading_img = cv.imread('./assets/cam1_opening.png')
            elif cam_id == 1:
                loading_img = cv.imread('./assets/cam2_opening.png')
            elif cam_id == 2:
                loading_img = cv.imread('./assets/cam3_opening.png')
            else:
                loading_img = cv.imread('./assets/cam3_opening.png')


            ret, img = cv.imencode('.jpg', loading_img)

            byte_img = img.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(byte_img) + b'\r\n')
        else:

            ret, buffer = cv.imencode('.jpg', frame)
            # frame을 byte로 변경 후 특정 식??으로 변환 후에
            # yield로 하나씩 넘겨준다.
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')


@app.get("/live/1")
def bird_detection():
    return StreamingResponse(read_cam(cam=cam_1, cam_id=0), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/live/2")
def bird_detection_2():
    return StreamingResponse(read_cam(cam=cam_2, cam_id=1), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/live/3")
def bird_detection_3():
    return StreamingResponse(read_cam(cam=cam_3, cam_id=2), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/live/4")
def bird_detection_4():
    return StreamingResponse(read_cam(cam=cam_4, cam_id=3), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/cmd/pipeline")
def bird_detection_5():
    return StreamingResponse(read_cam(cam_id=2), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/cmd/ext")
# EXTERMINATION
def bird_detection_6():
    return StreamingResponse(read_cam(cam_id=2), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    init_gpio()
    uvicorn.run(app, host="0.0.0.0", port=5000)

    # Works To Do::
    # 1. 다중 카메라 연동
    # 2. 캡처
    # 3. gpio 연동
    # 4. 서버 단에서 데이터 추론 후 교체 기능
