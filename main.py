import threading
from lane import Lane
from camera import Camera
import multiprocessing
from traffic_light import TrafficLight

# Define constants for lanes

if __name__ == "__main__":
    # Create lock for synchronizing access to shared resources
    lock = multiprocessing.Lock()
    
    # Create a multiprocessing manager to manage shared memory (a dictionary)
    with multiprocessing.Manager() as manager:
        # Shared dictionary to store vehicle count and total waiting time for each lane
        shared_memory = manager.dict({
            "south-north": [0, 0],  # [vehicle_count, total_waiting_time]
            "north-south": [0, 0],
            "west-east": [0, 0],
            "east-west": [0, 0],
            "south-east": [0, 0],
            "north-west": [0, 0],
            "west-south": [0, 0],
            "east-north": [0, 0],
        })

    # Create lanes (passing shared memory to each lane)
    lanes = [
        Lane(1, "south-north", 1, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(2, "north-south", 1, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(3, "west-east", 2, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(4, "east-west", 2, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(5, "south-east", 3, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(6, "north-west", 3, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(7, "west-souht", 4, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)]),
        Lane(8, "east-north", 4, [(123,345),(344,213), (123,345),(344,213), (123,345),(344,213), (123,345),(344,213)])
    ]

    # Create Camera processes for each lane
     # Create Camera processes for each lane, passing shared memory and lock
    camera1 = multiprocessing.Process(target=Camera("camera_ip", "username", "password", 8080, lanes[0], lanes[1], shared_memory, lock).monitor_lanes)
    camera2 = multiprocessing.Process(target=Camera("camera_ip", "username", "password", 8080, lanes[2], lanes[3], shared_memory, lock).monitor_lanes)
    camera3 = multiprocessing.Process(target=Camera("camera_ip", "username", "password", 8080, lanes[4], lanes[5], shared_memory, lock).monitor_lanes)
    camera4 = multiprocessing.Process(target=Camera("camera_ip", "username", "password", 8080, lanes[6], lanes[7], shared_memory, lock).monitor_lanes)

     # Create Traffic Light process, passing shared memory and lock
    traffic_light = multiprocessing.Process(target=TrafficLight(shared_memory, lock).adjust_traffic_light)

    # Start processes
    camera1.start()
    camera2.start()
    camera3.start()
    camera4.start()
    traffic_light.start()

    # Join processes (this will make sure the main process waits for them to finish)
    camera1.join()
    camera2.join()
    camera3.join()
    camera4.join()
    traffic_light.join()