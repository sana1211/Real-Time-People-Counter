# 👥 Real-Time People Counter

A real-time **People Detection, Tracking, and Counting System** built with **Python, YOLO11, OpenCV, and ByteTrack**.

The system detects people through a camera, tracks each person with a unique ID, and counts people entering and leaving an area using a vertical counting line.

---

## ✨ Features

* 👤 Real-time person detection
* 🎯 Person-only detection
* 🆔 Unique ID tracking for each person
* ➡️ **LEFT → RIGHT = IN**
* ⬅️ **RIGHT → LEFT = OUT**
* 📊 Total IN count
* 📊 Total OUT count
* 👥 Current number of people inside
* 📈 Real-time FPS display
* 🕐 Date and time display
* 📏 Configurable counting line
* 🚫 Ignores non-person objects
* ⚡ ByteTrack object tracking
* 📷 Webcam support
* 🖥️ Real-time OpenCV dashboard

---

## 🛠️ Technologies Used

| Technology  | Purpose                       |
| ----------- | ----------------------------- |
| Python      | Main programming language     |
| YOLO11      | Person detection              |
| Ultralytics | YOLO implementation           |
| OpenCV      | Camera processing and display |
| ByteTrack   | Person tracking               |
| NumPy       | Numerical processing          |

---

## 📁 Project Structure

```text
people-counter/
│
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignored files
│
├── models/
│   └── .gitkeep            # Model directory
│
├── screenshots/
│   └── .gitkeep            # Project screenshots
│
└── videos/
    └── .gitkeep            # Test videos
```

---

## 💻 Requirements

Before running the project, make sure you have:

* Python 3.9 or newer
* A webcam or compatible camera
* Windows / Linux / macOS
* Internet connection for installing Python packages

A GPU is **not required**, but a compatible NVIDIA GPU can improve performance.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/people-counter.git
```

Move into the project directory:

```bash
cd people-counter
```

---

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 YOLO Model

This project uses the:

```text
yolo11n.pt
```

YOLO11 Nano model.

The model is intentionally excluded from Git using `.gitignore`.

When the application starts, Ultralytics can download the required model automatically if it is not already available.

If you already have the model, place it in the project root:

```text
people-counter/
│
├── main.py
├── yolo11n.pt
├── requirements.txt
└── README.md
```

---

## ▶️ Running the Application

Activate your virtual environment first.

Then run:

```bash
python main.py
```

The webcam window will open automatically.

Press:

```text
Q
```

to close the application.

---

## 🎯 How People Counting Works

The system uses a vertical counting line positioned in the center of the camera frame.

```text
        OUTSIDE          SHOP INSIDE
             │
             │
             │
             │
             │
             │
        COUNTING LINE
```

### Entry

When a tracked person moves:

```text
LEFT → RIGHT
```

the system counts:

```text
IN +1
```

### Exit

When a tracked person moves:

```text
RIGHT → LEFT
```

the system counts:

```text
OUT +1
```

---

## 📊 Dashboard

The application displays:

```text
TOTAL IN
TOTAL OUT
CURRENT INSIDE
FPS
DATE
TIME
```

Example:

```text
┌─────────────────────────────────────────────┐
│              PEOPLE COUNTING                │
│                         2026-09-02 13:30:20 │
├─────────────────────────────────────────────┤
│                                             │
│       OUTSIDE       │       SHOP INSIDE     │
│                     │                       │
│                     │                       │
│                     │                       │
│                     │                       │
├─────────────────────┴───────────────────────┤
│                                             │
│     TOTAL OUT          TOTAL IN             │
│          2                  5                │
│                                             │
│              CURRENT INSIDE: 3              │
└─────────────────────────────────────────────┘
```

---

## 👤 Person-Only Detection

The system is configured to detect **people only**.

YOLO's COCO class:

```text
0 = person
```

The tracking configuration uses:

```python
classes=[0]
```

Therefore, objects such as:

* 🚗 Cars
* 🪑 Chairs
* 🎒 Bags
* 🧴 Bottles
* 📱 Phones
* 🐕 Animals

are not processed for people counting.

---

## ⚙️ Configuration

### Camera

The default camera is:

```python
cap = cv2.VideoCapture(0)
```

If your computer has multiple cameras, you can try:

```python
cap = cv2.VideoCapture(1)
```

or:

```python
cap = cv2.VideoCapture(2)
```

---

### Camera Resolution

The current resolution is:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

You can change it depending on your camera.

---

### Detection Confidence

The current confidence threshold is:

```python
conf=0.40
```

Increasing it can reduce weak detections.

For example:

```python
conf=0.50
```

---

### Counting Line Margin

The counting tolerance is:

```python
LINE_MARGIN = 25
```

This creates a small middle area around the counting line to help prevent accidental counting.

---

## 📱 Phone Camera Support

The project can also be adapted to use a phone camera as the camera source.

Instead of:

```python
cap = cv2.VideoCapture(0)
```

the camera source can be changed to a compatible network/stream URL.

Example:

```python
cap = cv2.VideoCapture("YOUR_CAMERA_STREAM_URL")
```

The exact URL depends on the phone-camera streaming method being used.

---

## 🔒 Git Security

Sensitive and unnecessary files should not be uploaded to GitHub.

The project `.gitignore` excludes:

```text
*.pt
venv/
__pycache__/
*.pyc
*.mp4
*.avi
*.mov
.env
```

This helps prevent large model files, virtual environments, videos, and secret environment files from being committed.

---

## 🧪 Troubleshooting

### Camera not found

If you see:

```text
Camera not found!
```

check:

1. Camera permissions
2. Camera connection
3. Whether another application is using the camera
4. Camera index (`0`, `1`, `2`, etc.)

---

### Low FPS

Try:

* Lowering camera resolution
* Using `yolo11n.pt`
* Using a GPU
* Closing other applications
* Reducing unnecessary processing

---

### Person not detected

Try lowering the confidence:

```python
conf=0.30
```

For stricter detection, increase it:

```python
conf=0.50
```

---

### Incorrect IN/OUT counting

Make sure the camera is positioned so that people clearly cross the counting line.

The default direction is:

```text
LEFT → RIGHT = IN

RIGHT → LEFT = OUT
```

---

## 🔮 Future Improvements

Possible future features include:

* 📱 Mobile camera integration
* 📹 Video recording
* 💾 Save daily statistics
* 📅 Daily/weekly/monthly reports
* 📊 Analytics dashboard
* 🗃️ Database integration
* 🌐 Web dashboard
* 🔔 Capacity alerts
* 📈 People-count graphs
* ☁️ Cloud data storage
* 🏪 Multi-camera support
* 🎥 CCTV/RTSP camera support
* 🔐 User authentication

---

## 📜 License

This project is intended for educational and development purposes.

You can modify and extend the project according to your requirements.

---

## 👨‍💻 Author

**Sankalpa Sugathsiri**

GitHub:
`https://github.com/YOUR_USERNAME`

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

### Made with ❤️ using Python, YOLO11 & OpenCV
