__author__ = 'Farai Rato'
__date__created = "01 May 2023"

from lane.lane_info import Lane
import time

# MQTT configuration
MQTT_BROKER = "localhost"  # Change to your broker address
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/light/state"


class TrafficLight:
    def __init__(self, shared_memory, lock):
        self.phase = 0
        self.phase_duration = 0
        self.shared_memory = shared_memory
        self.lock = lock

    def get_state(self, phase_duration,phase)-> list:
        """
        we define the state vector St as the queue length and waiting  time of vehicles ql in each lane l at
        time step t, in addition to the current phase of signals Pt. Queuing vehicles in the
        environment are those vehicles with speed less than 0.1 m/s.

        :param lanes_queues:
            queuing vehicles in each lane.
        :return:
            state -> [q1,q2,q3.., w1,w2,w3....], list
        """
        # Initialize empty lists for vehicle counts and waiting times
        vehicle_counts = []
        waiting_times = []

        # Iterate through the shared memory dictionary and extract the vehicle counts and waiting times
        for lane, data in self.shared_memory.items():
            vehicle_count, waiting_time = data  # Destructure the list into vehicle count and waiting time
            vehicle_counts.append(vehicle_count)  # Add vehicle count to the list
            waiting_times.append(waiting_time)  # Add waiting time to the list

        self.state = vehicle_counts + waiting_times
        self.state.append(phase)
        self.state.append(phase_duration)
        return self.state

    def get_reward(self)->int:
        """
        we define the reward function as the negative sum of queuing vehicles at time-step t
        stated as follows:
                      L−1
                Rt = − ∑ ql , where l is tha is the number of queued vehicles in each lane
                      l=0
        :return
            reward -> int
        """
        return -sum(self.state)

    def choose_action(self):
        """
        The action space is built-up of two hierarchical subspaces, respectively, of traffic
        light phases and the associated phase durations

        :return:
            action = (P, dp) : A = {{0, 1, 2, 3} ∪ {[t_min, t_max]}}, where P is the primary
            action which indicates a phase of the traffic signals and dP is the secondary parameter
            indicating the duration of the phase P.

        """
        pass

    def set_phase_duration(self):
        pass

    def get_phase(self):
        return self.get_phase
    
    def get_phase_duration(self):
        return self.get_phase_duration
    
    def adjust_traffic_light(self):
        
        while True:
             # Prepare the state to send (phase and phase duration)
                phase_data = {
                    "phase": self.phase,
                    "duration": self.phase_duration
                }
                
                # Publish phase and duration to MQTT topic
                self.publish_to_mqtt(phase_data)
    
    def publish_to_mqtt(self, phase_data):
        """Publish phase data to MQTT topic."""
        payload = f"Phase: {phase_data['phase']}, Duration: {phase_data['duration']}s"
        self.mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"Published to MQTT: {payload}")

    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker."""
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(MQTT_TOPIC)  # Subscribe to the topic if needed

    def on_message(self, client, userdata, msg):
        """Callback when a message is received on a subscribed topic."""
        print(f"Received message: {msg.payload.decode()}")
            
        
    
    
   



