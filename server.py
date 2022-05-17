import uvicorn, cv2, os

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

app = FastAPI()


templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024 * 1024


base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = base_path+"\\video"
if not os.path.exists(base_path):
    os.makedirs(base_path)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
record = False


def read_cam(cam_id=0):

    # camera 정의
    cam = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 15)

    if not cam.isOpened():
        if cam_id == 0:
            loading_img = cv2.imread('./assets/cam1_opening.png')
        elif cam_id == 1:
            loading_img = cv2.imread('./assets/cam2_opening.png')
        elif cam_id == 2:
            loading_img = cv2.imread('./assets/cam3_opening.png')

        ret, img = cv2.imencode('.jpg', loading_img)

        byte_img = img.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(byte_img) + b'\r\n')

    while cam.isOpened():
        # 카메라 값 불러오기
        success, frame = cam.read()

        if not success:

            if cam_id == 0:
                loading_img = cv2.imread('./assets/cam1_opening.png')
            elif cam_id == 1:
                loading_img = cv2.imread('./assets/cam2_opening.png')
            elif cam_id == 2:
                loading_img = cv2.imread('./assets/cam3_opening.png')

            ret, img = cv2.imencode('.jpg', loading_img)

            byte_img = img.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(byte_img) + b'\r\n')
        else:

            ret, buffer = cv2.imencode('.jpg', frame)
            # frame을 byte로 변경 후 특정 식??으로 변환 후에
            # yield로 하나씩 넘겨준다.
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')


@app.get("/live/1")
def bird_detection():
    return StreamingResponse(read_cam(cam_id=0), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/live/2")
def bird_detection_2():
    return StreamingResponse(read_cam(cam_id=1), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/live/3")
def bird_detection_3():
    return StreamingResponse(read_cam(cam_id=2), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/cmd/pipeline")
def bird_detection_4():
    return StreamingResponse(read_cam(cam_id=2), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

    # Works To Do::
    # 1. 다중 카메라 연동
    # 2. 캡처
    # 3. gpio 연동
    # 4. 서버 단에서 데이터 추론 후 교체 기능
