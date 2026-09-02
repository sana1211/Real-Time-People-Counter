from ultralytics import YOLO
import cv2
import time
from datetime import datetime


# ==========================================
# YOLO MODEL
# ==========================================

model = YOLO("yolo11n.pt")


# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ==========================================
# CHECK CAMERA
# ==========================================

if not cap.isOpened():
    print("Camera not found!")
    exit()


# ==========================================
# COUNTERS
# ==========================================

total_in = 0
total_out = 0


# ==========================================
# PERSON TRACKING
# ==========================================

person_sides = {}

LINE_MARGIN = 25


# ==========================================
# FPS
# ==========================================

previous_time = 0


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera frame not received!")
        break


    # ======================================
    # FRAME SIZE
    # ======================================

    height, width = frame.shape[:2]


    # ======================================
    # VERTICAL COUNTING LINE
    # ======================================

    line_x = width // 2


    # ======================================
    # FPS
    # ======================================

    current_time = time.time()

    if previous_time != 0:
        fps = 1 / (current_time - previous_time)
    else:
        fps = 0

    previous_time = current_time


    # ======================================
    # YOLO PERSON TRACKING ONLY
    # ======================================

    results = model.track(
        source=frame,

        # PERSON CLASS ONLY
        classes=[0],

        persist=True,

        tracker="bytetrack.yaml",

        conf=0.40,

        verbose=False
    )


    # ======================================
    # DRAW COUNTING LINE
    # ======================================

    cv2.line(
        frame,
        (line_x, 0),
        (line_x, height),
        (255, 0, 0),
        4
    )


    # ======================================
    # OUTSIDE LABEL
    # ======================================




    # ======================================
    # PERSON DETECTION
    # ======================================

    if (
        results[0].boxes is not None
        and results[0].boxes.id is not None
    ):

        boxes = results[0].boxes.xyxy.cpu().numpy()

        track_ids = (
            results[0]
            .boxes
            .id
            .cpu()
            .numpy()
            .astype(int)
        )

        class_ids = (
            results[0]
            .boxes
            .cls
            .cpu()
            .numpy()
            .astype(int)
        )


        # ==================================
        # PROCESS PERSONS ONLY
        # ==================================

        for box, track_id, class_id in zip(
            boxes,
            track_ids,
            class_ids
        ):

            # --------------------------------
            # PERSON CLASS = 0
            # --------------------------------

            if class_id != 0:
                continue


            # ==================================
            # PERSON BOX
            # ==================================

            x1, y1, x2, y2 = map(int, box)


            # ==================================
            # CENTER POINT
            # ==================================

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2


            # ==================================
            # DRAW PERSON BOX
            # ==================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # ==================================
            # DRAW CENTER POINT
            # ==================================

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )


            # ==================================
            # PERSON LABEL
            # ==================================

            cv2.putText(
                frame,
                f"PERSON ID {track_id}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


            # ==================================
            # DETERMINE PERSON SIDE
            # ==================================

            if center_x < line_x - LINE_MARGIN:

                current_side = "LEFT"

            elif center_x > line_x + LINE_MARGIN:

                current_side = "RIGHT"

            else:

                current_side = "MIDDLE"


            # ==================================
            # FIRST TIME PERSON DETECTED
            # ==================================

            if track_id not in person_sides:

                if current_side != "MIDDLE":

                    person_sides[track_id] = current_side


            # ==================================
            # EXISTING PERSON
            # ==================================

            else:

                previous_side = person_sides[track_id]


                # ==================================
                # LEFT -> RIGHT = IN
                # ==================================

                if (
                    previous_side == "LEFT"
                    and current_side == "RIGHT"
                ):

                    total_in += 1

                    person_sides[track_id] = "RIGHT"

                    print(
                        f"Person {track_id} ENTERED"
                    )


                # ==================================
                # RIGHT -> LEFT = OUT
                # ==================================

                elif (
                    previous_side == "RIGHT"
                    and current_side == "LEFT"
                ):

                    total_out += 1

                    person_sides[track_id] = "LEFT"

                    print(
                        f"Person {track_id} EXITED"
                    )


                # ==================================
                # UPDATE SIDE
                # ==================================

                elif current_side != "MIDDLE":

                    person_sides[track_id] = current_side


    # ==========================================
    # CURRENT INSIDE
    # ==========================================

    current_inside = total_in - total_out

    if current_inside < 0:
        current_inside = 0


    # ==========================================
    # DATE & TIME
    # ==========================================

    now = datetime.now()

    date_text = now.strftime("%Y-%m-%d")

    time_text = now.strftime("%H:%M:%S")


    # ==========================================
    # TOP TITLE BAR
    # ==========================================

    cv2.rectangle(
        frame,
        (0, 0),
        (width, 80),
        (0, 110, 0),
        -1
    )


    cv2.putText(
        frame,
        "PEOPLE COUNTING",
        (40, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3
    )


    # ==========================================
    # DATE / TIME
    # ==========================================

    cv2.putText(
        frame,
        f"{date_text}  {time_text}",
        (width - 300, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    # ==========================================
    # FPS
    # ==========================================

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    # ==========================================
    # BOTTOM DASHBOARD
    # ==========================================

    dashboard_height = 150

    dashboard_y = height - dashboard_height


    # Dashboard background
    cv2.rectangle(
        frame,
        (0, dashboard_y),
        (width, height),
        (30, 30, 30),
        -1
    )


    # ==========================================
    # OUT PANEL
    # ==========================================

    cv2.rectangle(
        frame,
        (20, dashboard_y + 15),
        (width // 2 - 10, height - 15),
        (80, 0, 0),
        -1
    )


    # ==========================================
    # IN PANEL
    # ==========================================

    cv2.rectangle(
        frame,
        (width // 2 + 10, dashboard_y + 15),
        (width - 20, height - 15),
        (0, 100, 0),
        -1
    )


    # ==========================================
    # OUT TEXT
    # ==========================================

    cv2.putText(
        frame,
        "TOTAL OUT",
        (60, dashboard_y + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        3
    )


    # ==========================================
    # OUT NUMBER
    # ==========================================

    cv2.putText(
        frame,
        str(total_out),
        (250, dashboard_y + 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        2.0,
        (255, 255, 255),
        4
    )


    # ==========================================
    # IN TEXT
    # ==========================================

    cv2.putText(
        frame,
        "TOTAL IN",
        (width // 2 + 50, dashboard_y + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        3
    )


    # ==========================================
    # IN NUMBER
    # ==========================================

    cv2.putText(
        frame,
        str(total_in),
        (width // 2 + 230, dashboard_y + 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        2.0,
        (255, 255, 255),
        4
    )


    # ==========================================
    # CURRENT INSIDE
    # ==========================================

    cv2.putText(
        frame,
        f"CURRENT INSIDE: {current_inside}",
        (width // 2 - 120, dashboard_y + 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )


    # ==========================================
    # SHOW CAMERA
    # ==========================================

    cv2.imshow(
        "Real-Time People Counter",
        frame
    )


    # ==========================================
    # PRESS Q TO EXIT
    # ==========================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# RELEASE CAMERA
# ==========================================

cap.release()

cv2.destroyAllWindows()