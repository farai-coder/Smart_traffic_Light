import time

class Vehicle:
    def __init__(self, vehicle_id, bbox):
        """
        Initializes a new vehicle object.

        Args:
            vehicle_id (int): Unique identifier for the vehicle.
            bbox (list): Bounding box coordinates in the format [x1, y1, x2, y2].
        """
        self.vehicle_id = vehicle_id  # Vehicle ID
        self.bbox = bbox  # [x1, y1, x2, y2] (bounding box coordinates)
        self.entry_time = time.time()  # Time when vehicle was first detected
        self.waiting_time = 0  # Accumulated waiting time in seconds
        self.is_escaped = False  # Flag to check if the vehicle has escaped
        self.last_seen_time = self.entry_time  # Time of last detection
    
    def accumulate_waiting_time(self):
        """
        Accumulates the waiting time if the vehicle has not escaped.
        Updates the last seen time to the current time.

        This method is typically called at regular intervals to track the 
        waiting time of a vehicle.
        """
        if not self.is_escaped:
            time_elapsed = time.time() - self.last_seen_time
            
            # If the time elapsed since the last detection is greater than 10 seconds, mark as escaped
            if time_elapsed > 15:
                self.is_escaped = True
            self.waiting_time = time.time() - self.entry_time
            self.set_last_seen_time(self) # update the last seen time
    
    def get_waiting_time(self):
        """
        Returns the accumulated waiting time for the vehicle.

        Returns:
            float: The waiting time in seconds.
        """
        return self.waiting_time
    
    def set_is_escaped(self, status):
        """
        Sets the escape status of the vehicle.

        Args:
            status (bool): True if the vehicle is escaped, False otherwise.
        """
        self.is_escaped = status
    
    # Getter for is_escaped
    def get_is_escaped(self):
        """
        Returns the escape status of the vehicle.

        Returns:
            bool: True if the vehicle is escaped, False otherwise.
        """
        return self.is_escaped
    
    # Getter for last_seen_time
    def get_last_seen_time(self):
        return self.last_seen_time

    # Setter for last_seen_time
    def set_last_seen_time(self):
        self.last_seen_time = time.time()

    def update_bbox(self, bbox):
        """
        Updates the bounding box coordinates for the vehicle.

        Args:
            bbox (list): New bounding box coordinates in the format [x1, y1, x2, y2].
        """
        self.bbox = bbox
        
    def get_bbox(self):
        """
        Returns the current bounding box coordinates of the vehicle.

        Returns:
            list: The current bounding box coordinates in the format [x1, y1, x2, y2].
        """
        return self.bbox
