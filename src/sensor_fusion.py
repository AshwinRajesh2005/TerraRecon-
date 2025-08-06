import numpy as np
from motor_control import get_distance_cm

class SensorFusion:
    """Combines data from LIDAR and ultrasonic sensors for navigation."""
    def __init__(self):
        self.lidar_data = None  # Placeholder for LIDAR point cloud
        self.ultrasonic_distance = float('inf')

    def update_lidar_data(self, point_cloud):
        """Updates LIDAR point cloud data."""
        self.lidar_data = point_cloud  # Expected to be a numpy array of 3D points
        print("SIMULATION: Updated LIDAR point cloud.")

    def update_ultrasonic_data(self):
        """Updates ultrasonic sensor data."""
        self.ultrasonic_distance = get_distance_cm()
        print(f"Ultrasonic distance updated: {self.ultrasonic_distance:.1f} cm")

    def fuse_sensors(self):
        """Combines LIDAR and ultrasonic data for obstacle detection."""
        if self.lidar_data is None:
            print("WARNING: No LIDAR data available. Using ultrasonic data only.")
            return self.ultrasonic_distance < 30  # Threshold from config
        # Simplified fusion: Check if either sensor detects an obstacle
        lidar_obstacle = np.any(self.lidar_data[:, 2] < 0.3) if self.lidar_data is not None else False
        ultrasonic_obstacle = self.ultrasonic_distance < 30
        return lidar_obstacle or ultrasonic_obstacle

    def get_navigation_decision(self):
        """Returns navigation decision based on fused sensor data."""
        if self.fuse_sensors():
            return "STOP"  # Obstacle detected
        return "MOVE_FORWARD"  # Safe to proceed