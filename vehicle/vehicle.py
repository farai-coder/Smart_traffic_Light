import time 



class Vehicle:
    def __init__(self, vehicle_id, bbox):
        self.vehicle_id = vehicle_id  # Vehicle ID
        self.bbox = bbox  # [x1, y1, x2, y2] (bounding box coordinates)
        self.entry_time = time.time()  # Time when vehicle was first detected
        self.waiting_time = 0  # Accumulated waiting time in seconds
        self.is_escaped = False  # Flag to check if the vehicle has escaped
        self.last_seen_time = self.entry_time  # Time of last detection
    
    def accumulate_waiting_time(self):
        """ Accumulate the waiting time. """
        if not self.is_escaped:
            self.waiting_time = time.time() - self.entry_time
            self.last_seen_time = time.time()  # Update last seen time
    
    def get_waiting_time(self):
        return self.waiting_time
    
    def escape(self):
        """ Mark the vehicle as escaped and calculate the final waiting time. """
        self.is_escaped = True
        self.waiting_time += time.time() - self.last_seen_time  # Add time after last detection
        return self.waiting_time
