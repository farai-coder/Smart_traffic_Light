__author__ = 'Farai Rato'
__date__created = "01 May 2023"

class Lane:
    
    def __init__(self, lane_id, lane_name, lane_phase):
        self.lane_ID = lane_id
        self.lane_name = lane_name
        self.lane_phase = lane_phase
        self.total_waiting_time = 0
        self.vehicles_count = 0
        
    def accumulate_waiting_time(self, VEHICLE_LIST):
        self.total_waiting_time += sum(vehicle.get_waiting_time() for vehicle in VEHICLE_LIST)

    def queued_vehicles(self,vehicle_counts):
        total_vehicles = sum(vehicle_counts[vehicle_type] for vehicle_type in vehicle_counts)

    def get_waiting_time(self) -> float:
        return self.total_waiting_time
    
    def get_vehicle_count(self) -> int:
        return self.vehicles_count
    
    def get_lane_name(self):
        return self.lane_name
    
    def get_lane_phase(self):
        return self.lane_phase

    def clear_leaving_vehicles(self,tracking_list, light_position):
        pass
