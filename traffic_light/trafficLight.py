__author__ = 'Farai Rato'
__date__created = "01 May 2023"

from lane.lane_info import Lane

class TrafficLight:
    def __init__(self):

        pass

    def get_state(self,ALL_LANES: list, phase_duration,phase)-> list:
        """
        we define the state vector St as the queue length and waiting  time of vehicles ql in each lane l at
        time step t, in addition to the current phase of signals Pt. Queuing vehicles in the
        environment are those vehicles with speed less than 0.1 m/s.

        :param lanes_queues:
            queuing vehicles in each lane.
        :return:
            state -> [q1,q2,q3.., w1,w2,w3....], list
        """
        for lane_info in ALL_LANES:
            self.state.append(self.lane.queued_vehicles_in_lane(lane_info))
        for lane_info in ALL_LANES:
            self.state.append(self.lane.waiting_time_in_lane(lane_info))

        self.state.append(phase_duration)
        self.state.append(phase)

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

    def GPIO(self):
        """
        We are using this to control the traffic lights and the count-down timers.

        """
        pass



