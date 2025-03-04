import numpy as np
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from vehicle.vehicle import Vehicle
import time

model = YOLO("yolov8n.pt")
lane1 = [(465,230),(595,230),(968,999),(470,886)]
url = 'sample.mp4'

tracker = DeepSort(max_age=5,
                   n_init=2,
                   nms_max_overlap=1.0,
                   max_cosine_distance=0.3,
                   nn_budget=None,
                   override_track_class=None,
                   embedder="mobilenet",
                   half=True,
                   bgr=True,
                   embedder_gpu=True,
                   embedder_model_name=None,
                   embedder_wts=None,
                   polygon=False,
                   today=None)

def draw_boxes(frame, bbox, identities=None, model = "", categories=None, label='' ,names=None, offset=(0,0)):
    x1,y1,x2,y2 = bbox
    cv2.rectangle(frame, (x1, y1), (x2,y2), color= (15,220,10), thickness=1)
    cv2.putText(frame, str(label), (x1, y1-2), 0, 1/2, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
    return frame

def print_tracking_list(tracking_list):
    """Print tracking list in dictionary format with ID, bounding box, and waiting time."""
    if not tracking_list:
        print("No vehicles are currently being tracked.")
        return

    # Create a dictionary to hold the data in the desired format
    tracking_info = {}

    for track_id, vehicle in tracking_list.items():
        
        tracking_info[track_id] = {
            "bounding_box": vehicle.bbox,
            "entry_time" : vehicle.entry_time,
            "current_time": time.time(),
            "waiting_time": vehicle.get_waiting_time(),
            "waiting_time2": time.time() - vehicle.entry_time
        }

    # Print the tracking info as a dictionary
    print(tracking_info)

cap = cv2.VideoCapture(url)
count = 0
tracking_list = {}
vehicles = [2,3,5,7]  # Assuming these are class IDs for cars, buses, trucks, etc.
vehicle_counts = {"total": 0, "cars": 0, "buses": 0, "trucks": 0}

class_mapping = {2: "cars", 3: "buses", 5: "trucks"}

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (920,630))

    if not ret:
        break
    if count % 3== 0:
        count = 0
        results = model.predict(source=frame,show=False)
        vehicle_counts["total"] = 0
        vehicle_counts["cars"] = 0
        vehicle_counts["buses"] = 0
        vehicle_counts["trucks"] = 0
        
        for result in results:
            detections = []
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2 , score, class_id = r
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                score = float(score)
                class_id = int(class_id)
                if class_id in vehicles:
                    detections.append((([x1, y1, abs(x1-x2), abs(y1-y2)]) , score, class_id))
                    
                    # Update vehicle counts
                    vehicle_counts["total"] += 1
                    if class_id in class_mapping:
                        vehicle_counts[class_mapping[class_id]] += 1

            tracks = tracker.update_tracks(detections,frame=frame)
            for track in tracks:
                Itrb = track.to_ltrb()
                if track.is_confirmed:
                    x1, y1, x2, y2 = Itrb
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    track_id = track.track_id

                    if track_id not in tracking_list:
                        vehicle = Vehicle(track_id, [x1,y1,x2,y2])
                        tracking_list[track_id] = vehicle
                    else:
                        tracking_list[track_id].bbox = [x1,y1,x2,y2]
                        tracking_list[track_id].accumulate_waiting_time()
                    
                    frame = draw_boxes(frame = frame,bbox=[x1,y1,x2,y2],model=model,label = track_id)
                
                else:
                    print("track not confirmed...........")
                    track_id = track.track_id
                    if track_id in tracking_list:
                        del tracking_list[track_id]
                    
            # Display vehicle counts on the frame
            cv2.putText(frame, f'Total Vehicles: {vehicle_counts["total"]}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f'Cars: {vehicle_counts["cars"]}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f'Buses: {vehicle_counts["buses"]}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f'Trucks: {vehicle_counts["trucks"]}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            cv2.imshow("frame", frame)
                    
        # Call the function to print the tracking list
        #print_tracking_list(tracking_list)
        
    count += 1
    cv2.waitKey(1)
cv2.destroyAllWindows()
cap.release()
