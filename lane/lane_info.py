__author__ = 'Farai Rato'
__date__created = "01 May 2023"
import cv2
import numpy as np

class Lane:
    
    def __init__(self, lane_id, lane_name, lane_phase, area):
        """
        Initializes a new Lane object.

        Args:
            lane_id (int): Unique identifier for the lane.
            lane_name (str): The name of the lane.
            lane_phase (str): The phase associated with the lane (e.g., green, red).
            area (list): The polygonal area of the lane defined by coordinates.
        """
        self.lane_ID = lane_id
        self.lane_name = lane_name
        self.lane_phase = lane_phase
        self.total_waiting_time = 0
        self.vehicles_count = 0
        self.vehicles_list = {}
        self.area = area
    
    def map_vehicle_into_lane(self, vehicle):
        """
        Maps a vehicle into the lane based on its bounding box.

        Args:
            vehicle (Vehicle): The vehicle object that needs to be mapped into the lane.

        Returns:
            bool: True if the vehicle is within the lane's area, False otherwise.
        """
        x1, y1, x2, y2 = vehicle.get_bbox()  # Calculate the center of the vehicle
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        if cv2.pointPolygonTest(np.array([self.area]), (center_x, center_y), False) == 1:
            return True
        else:
            return False
        
    def update_vehicles_list(self, vehicle, track_id, bbox):
        """
        Updates the list of vehicles in the lane. If the vehicle is new and inside the lane,
        it is added to the list. If the vehicle is already in the list, its waiting time is accumulated.

        Args:
            vehicle (Vehicle): The vehicle object to update.
            track_id (int): Unique identifier for the vehicle's track.
            bbox (list): The bounding box of the vehicle in the format [x1, y1, x2, y2].
        """
        if track_id not in self.vehicles_list and self.map_vehicle_into_lane(vehicle) == True:
            self.vehicles_list[track_id] = vehicle
            vehicle.update_bbox(bbox)
            
        elif track_id in self.vehicles_list and self.map_vehicle_into_lane(vehicle) == True:
            self.vehicles_list[track_id].accumulate_waiting_time()
        
    def get_vehicles_list(self) -> list:
        """
        Returns the list of vehicles currently in the lane.

        Returns:
            list: List of vehicles in the lane.
        """
        return self.vehicles_list        
        
    def accumulate_total_waiting_time(self):
        """
        Accumulates the total waiting time for all vehicles in the lane.
        """
        self.total_waiting_time += sum(vehicle.get_waiting_time() for vehicle in self.vehicles_list)

    def queued_vehicles(self, vehicle_counts):
        """
        Calculates the total number of queued vehicles in the lane.

        Args:
            vehicle_counts (dict): A dictionary with vehicle types as keys and their counts as values.
        """
        total_vehicles = sum(vehicle_counts[vehicle_type] for vehicle_type in vehicle_counts)

    def get_waiting_time(self) -> float:
        """
        Returns the total accumulated waiting time for the lane.

        Returns:
            float: The total waiting time in seconds.
        """
        return self.total_waiting_time
    
    def get_vehicle_count(self) -> int:
        """
        Returns the total number of vehicles in the lane.

        Returns:
            int: The number of vehicles in the lane.
        """
        return self.vehicles_count
    
    def get_lane_name(self):
        """
        Returns the name of the lane.

        Returns:
            str: The name of the lane.
        """
        return self.lane_name
    
    def get_lane_phase(self):
        """
        Returns the phase of the lane (e.g., red, green).

        Returns:
            str: The phase of the lane.
        """
        return self.lane_phase

    def clear_leaving_vehicles(self, track_id):
        """
        function for clearing leaving vehicles. 
        is used when vehicles leave the lane.

        Args:
            tracking_list (list): The list of active tracked vehicles..
        """
        del self.vehicles_list[track_id]
