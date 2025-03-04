__author__ = 'Farai Rato'
__date__created = "01 May 2023"

import cv2
from configs import *
import numpy as np

def vehicles_into_lanes(vehicle_id, vehicle):
    """
    This is mapping every vehicle into its lane.

    :param vehicle[0]:
        the bounding box of a vehicle
    """
    x1, y1, x2, y2 = vehicle # calculate the center of the vehicle
    center_x = (x1 + x2)/2
    center_y = (y1 + y2)/2

    if cv2.pointPolygonTest(np.array([AREA_1]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_1:
        LANE_1.append(vehicle_id)

    elif cv2.pointPolygonTest(np.array([AREA_2]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_2:
        LANE_2.append(vehicle_id)

    elif  cv2.pointPolygonTest(np.array([AREA_3]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_3:
        LANE_3.append(vehicle_id)

    elif cv2.pointPolygonTest(np.array([AREA_4]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_4:
        LANE_4.append(vehicle_id)

    elif  cv2.pointPolygonTest(np.array([AREA_5]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_5:
        LANE_5.append(vehicle_id)

    elif cv2.pointPolygonTest(np.array([AREA_6]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_6:
        LANE_6.append(vehicle_id)

    elif cv2.pointPolygonTest(np.array([AREA_7]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_7:
        LANE_7.append(vehicle_id)

    elif cv2.pointPolygonTest(np.array([AREA_8]),(center_x, center_y),False) == 1 and vehicle_id not in LANE_8:
        LANE_8.append(vehicle_id)





