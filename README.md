Smart Traffic Light System with YOLO and DeepSORT
Overview
This project implements a smart traffic light system that uses YOLO (You Only Look Once) for real-time vehicle detection and DeepSORT for object tracking. The system can adjust traffic light phases based on the number of vehicles and their waiting times in the lanes. Multiple cameras monitor each lane of the traffic, and the system manages the traffic light phases dynamically.

The system can be further enhanced by integrating Deep Q-Learning (DQN) for optimal traffic light phase decisions based on real-time traffic data.

Features
Real-time vehicle detection using YOLOv5.
Vehicle tracking using DeepSORT across camera frames.
Dynamic traffic light management based on lane data (vehicle count and waiting time).
Multiple camera support: Each camera monitors a different lane.
Concurrent camera processing using multithreading.
Project Structure
bash
Copy
├── camera.py          # Camera class for vehicle detection and tracking
├── lane.py            # Lane class to manage lane-specific data (vehicles, waiting time, etc.)
├── vehicle.py         # Vehicle class to manage vehicle-related data
├── traffic_light.py   # TrafficLight class for traffic light management and phase adjustment
├── main.py            # Main script to run the traffic light system
├── requirements.txt   # Required libraries and dependencies
└── README.md          # Project documentation
Setup Instructions
Prerequisites
Before running the project, make sure you have the following:

Python 3.x installed.
A working camera (or video stream) to test the vehicle detection and tracking.
A pre-trained YOLOv5 model. You can use the official YOLOv5 small model (yolov5s.pt).
Step 1: Install Dependencies
Clone the repository and install the required dependencies.

bash
Copy
git clone https://github.com/farai-coder/Smart_Traffic_Light-system.git
cd smart-traffic-light-system
pip install -r requirements.txt
Create a requirements.txt file with the following content:

txt
Copy
opencv-python
opencv-python-headless
numpy
tensorflow
deep_sort_realtime
yolov5
Step 2: Download YOLOv5 Model
Download the pre-trained YOLOv5 model (e.g., yolov5s.pt) from the official YOLOv5 repo and place it in the project directory.

Alternatively, you can modify the Camera class to point to the model file in your setup.

Step 3: Run the Traffic Light System
To run the system, execute the following command:

bash
Copy
python main.py
The system will start processing the camera feeds, detecting and tracking vehicles in real-time, and adjusting the traffic light phases based on the vehicle data. Press 'q' to exit the camera view.

Code Explanation
Vehicle Class
The Vehicle class stores the vehicle's unique ID, entry time, and waiting time. It also includes methods for updating and retrieving vehicle data.

Lane Class
The Lane class stores information about a specific lane, including the vehicles waiting in the lane, the total waiting time, and the vehicle count. It allows adding/removing vehicles and updating the lane's waiting time.

Camera Class
The Camera class is responsible for capturing frames from the video feed, detecting vehicles using YOLOv5, and tracking them using DeepSORT. It updates the lane with vehicle IDs and displays the current frame with bounding boxes around the tracked vehicles.

TrafficLight Class
The TrafficLight class manages the traffic light system. It collects lane data (vehicle count and waiting time) and decides the traffic light phases. Currently, it uses a placeholder function for phase decision-making, but this can be replaced with a Deep Q-Learning model for dynamic phase adjustment.

Main Script
The main.py script initializes lanes, cameras, and the traffic light system. It runs each camera in a separate thread and periodically adjusts the traffic light phase based on the collected lane data.

Enhancements
Deep Q-Learning (DQN): You can integrate a DQN model to make real-time decisions about traffic light phases based on the queue lengths and waiting times.
Data Logging: Implement data logging to track vehicle count, waiting times, and phase durations for analysis.
Multiple Cameras: Add support for additional cameras if required, for monitoring more lanes.
Troubleshooting
1. Camera not detected
Make sure the camera is properly connected and accessible. If you're using a video file or stream, update the cv2.VideoCapture() argument accordingly.

2. YOLOv5 model not found
Ensure you have downloaded the YOLOv5 model (e.g., yolov5s.pt) and placed it in the project directory. Update the path in the Camera class if necessary.

License
This project is licensed under the MIT License - see the LICENSE file for details.
