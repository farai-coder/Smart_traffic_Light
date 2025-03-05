import numpy as np
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from vehicle import Vehicle
import time
from onvif import ONVIFCamera

model = YOLO("yolov8n.pt")

class Camera:
    def __init__(self, camera_ip, username, password, camera_port, straight_lane, turning_lane, shared_memory, lock):
        """
        Initialize the camera object with required parameters.
        
        Args:
            camera_ip (str): The IP address of the camera.
            username (str): The username for authentication.
            password (str): The password for authentication.
            camera_port (int): The port number of the camera.
            straight_lane (Lane): The straight lane object to monitor.
            turning_lane (Lane): The turning lane object to monitor.
            shared_memory (multiprocessing.Manager.dict): Shared memory to store vehicle data.
            lock (multiprocessing.Lock): Lock for synchronizing access to shared memory.
        """
        self.camera_ip = camera_ip
        self.username = username
        self.password = password
        self.camera_port = camera_port
        self.straight_lane = straight_lane
        self.turning_lane = turning_lane
        self.url = ""
        self.shared_memory = shared_memory
        self.lock = lock

        # Initialize the vehicle tracker (DeepSort)
        self.tracker = DeepSort(
            max_age=5,
            n_init=2,
            nms_max_overlap=1.0,
            max_cosine_distance=0.3,
            nn_budget=None,
            embedder="mobilenet",
            half=True,
            bgr=True,
            embedder_gpu=True
        )
        
        # Initialize the tracking dictionary and vehicle count
        self.vehicle_counts = {"total": 0, "cars": 0, "buses": 0, "trucks": 0}
        self.class_mapping = {2: "cars", 3: "buses", 5: "trucks"}
        
    def set_url(self):
        """
        Set the RTSP URL for the camera stream.
        Uses ONVIF to retrieve the RTSP stream URI.
        """
        camera = ONVIFCamera(self.camera_ip, self.camera_port, self.username, self.password)

        # Get the media service
        media_service = camera.create_media_service()

        # Get the available profiles (each camera will have one or more video profiles)
        profiles = media_service.GetProfiles()

        # Choose the first profile (you can choose another if needed)
        profile = profiles[0]

        # Get the RTSP stream URI from the camera's media service
        stream_uri = media_service.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken': profile.token})

        # Print the RTSP URL
        self.url = stream_uri.Uri
        
    def draw_boxes(self, frame, bbox, identities=None, model=None, label='', names=None, offset=(0, 0)):
        """
        Draw bounding boxes on the frame and label the detected vehicles.
        
        Args:
            frame (ndarray): The video frame to draw on.
            bbox (list): The bounding box coordinates [x1, y1, x2, y2].
            identities (list): Optional list of vehicle identities.
            model (any): Optional model parameter.
            label (str): The label to display on the bounding box.
            names (list): Optional list of class names.
            offset (tuple): The offset for drawing the label.
        
        Returns:
            ndarray: The frame with bounding boxes drawn.
        """
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(15, 220, 10), thickness=1)
        cv2.putText(frame, str(label), (x1, y1 - 2), 0, 1 / 2, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        return frame
    
    def print_tracking_list(self, tracking_list):
        """
        Print tracking list in dictionary format with ID, bounding box, and waiting time.
        
        Args:
            tracking_list (dict): The list of tracked vehicles.
        """
        if not tracking_list:
            print("No vehicles are currently being tracked.")
            return

        # Create a dictionary to hold the data in the desired format
        tracking_info = {}

        for track_id, vehicle in tracking_list.items():
            tracking_info[track_id] = {
                "bounding_box": vehicle.bbox,
                "entry_time": vehicle.entry_time,
                "current_time": time.time(),
                "waiting_time": vehicle.get_waiting_time(),
                "waiting_time2": time.time() - vehicle.entry_time
            }

        # Print the tracking info as a dictionary
        print(tracking_info)
        
    def update_shared_memory_count(self, lane):
        """
        Update the shared memory with vehicle count.
        
        Args:
            vehicle_count (int): The count of vehicles in the lane.
            lane (Lane): The lane object to update the count for.
        """
        with self.lock:
            self.shared_memory[lane.lane_name][0] = lane.get_vehicle_count()
    
    def update_shared_memory_waiting_time(self, lane):
        """
        Update the shared memory with the waiting time of vehicles in the lane.
        
        Args:
            waiting_time (float): The total waiting time of vehicles in the lane.
            lane_name (str): The name of the lane to update.
        """
        with self.lock:
            self.shared_memory[lane.lane_name][1] = lane.waiting_time()

    def monitor_lanes(self):
        """
        Monitor the lanes by capturing frames from the camera, running object detection with YOLO, 
        tracking vehicles with DeepSort, and updating shared memory with vehicle counts and waiting times.
        """
        self.set_url()
        cap = cv2.VideoCapture(self.url)
        count = 0
        
        # Initialize the loop for reading frames from the video
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, (920, 630))

            if not ret:
                break

            if count % 3 == 0:  # Only process every 3rd frame to speed up
                count = 0

                # Run YOLO model to predict vehicle bounding boxes
                results = model.predict(source=frame, show=False)
                
                # Reset vehicle counts for each frame
                self.vehicle_counts["total"] = 0
                self.vehicle_counts["cars"] = 0
                self.vehicle_counts["buses"] = 0
                self.vehicle_counts["trucks"] = 0

                detections = []

                # Extract bounding boxes and class information from YOLO results
                for result in results:
                    for r in result.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = r
                        x1 = int(x1)
                        y1 = int(y1)
                        x2 = int(x2)
                        y2 = int(y2)
                        score = float(score)
                        class_id = int(class_id)

                        if class_id in self.class_mapping.keys():  # Filter based on relevant vehicle classes
                            detections.append(([x1, y1, abs(x1 - x2), abs(y1 - y2)] , score, class_id))
                            
                            # Update vehicle counts
                            self.vehicle_counts["total"] += 1
                            self.lane.queued_vehicles(self.vehicle_counts)
                            
                            if class_id in self.class_mapping:
                                self.vehicle_counts[self.class_mapping[class_id]] += 1

                # Update tracking for detected vehicles
                tracks = self.tracker.update_tracks(detections, frame=frame)

                for track in tracks:
                    Itrb = track.to_ltrb()

                    if track.is_confirmed:
                        x1, y1, x2, y2 = Itrb
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        track_id = track.track_id
                        
                        vehicle = Vehicle(track_id, [x1, y1, x2, y2])
                        
                        self.straight_lane.clear_leaving_vehicles()
                        self.turning_lane.clear_leaving_vehicles()
                        self.straight_lane.update_vehicles_list(vehicle, track_id, [x1, y1, x2, y2])  # monitor vehicles in lane
                        self.turning_lane.update_vehicles_list(vehicle, track_id, [x1, y1, x2, y2])
 
                        #update the shared memory for this camera with the total waiting and vehicle count time in the lane
                        self.update_shared_memory_waiting_time(self.straight_lane.get_waiting_time(), self.straight_lane.get_lane_name())
                        self.update_shared_memory_waiting_time(self.turning_lane.get_waiting_time(), self.turning_lane.get_lane_name())
                        self.update_shared_memory_count(self.straight_lane.get_vehicle_count(), self.straight_lane)
                        self.update_shared_memory_count(self.turning_lane.get_vehicle_count(), self.turning_lane)

                        # Draw the tracked boxes and ID labels on the frame
                        frame = self.draw_boxes(frame=frame, bbox=[x1, y1, x2, y2], label=track_id)

                    else:
                        track_id = track.track_id
                        if track_id in self.tracking_list:
                            del self.tracking_list[track_id]

                # Display vehicle counts on the frame
                cv2.putText(frame, f'Total Vehicles: {self.vehicle_counts["total"]}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, f'Cars: {self.vehicle_counts["cars"]}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, f'Buses: {self.vehicle_counts["buses"]}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, f'Trucks: {self.vehicle_counts["trucks"]}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cv2.imshow("frame", frame)

            count += 1
            cv2.waitKey(1)

        # Clean up and release video capture
        cv2.destroyAllWindows()
        cap.release()
