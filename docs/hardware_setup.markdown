# TerraRecon Hardware Setup Guide

This guide outlines the steps to assemble and configure the hardware for the TerraRecon autonomous surveillance rover.

## Components
- **Raspberry Pi 4**: Main controller (4GB or 8GB RAM recommended).
- **LIDAR Sensor**: For environment mapping (e.g., RPLIDAR A1).
- **Infrared Camera**: For low-light vision (e.g., Raspberry Pi NoIR Camera Module).
- **Ultrasonic Sensor**: For obstacle detection (e.g., HC-SR04).
- **GPS Module**: For navigation (e.g., NEO-6M).
- **DC Motors with Drivers**: For movement (e.g., L298N motor driver with 4 DC motors).
- **Chassis**: 3D-printed with modular tracks for terrain adaptability.
- **Power Supply**: 12V battery pack with 5V regulator for Raspberry Pi.
- **RF Module**: For long-range communication (e.g., NRF24L01).

## Assembly Steps
1. **Prepare the Chassis**:
   - Assemble the 3D-printed chassis and attach tracks.
   - Mount DC motors securely to the chassis.
2. **Connect Motors to Driver**:
   - Wire motors to the L298N motor driver.
   - Connect driver pins to Raspberry Pi GPIO:
     - Left Forward: GPIO 17
     - Left Backward: GPIO 27
     - Right Forward: GPIO 22
     - Right Backward: GPIO 23
     - Left Enable: GPIO 18
     - Right Enable: GPIO 24
3. **Attach Sensors**:
   - Connect ultrasonic sensor:
     - Trigger: GPIO 25
     - Echo: GPIO 8
   - Connect LIDAR to Raspberry Pi via USB or GPIO (refer to sensor manual).
   - Attach infrared camera to the Raspberry Pi camera port.
   - Connect GPS module to UART pins (e.g., GPIO 14, 15).
4. **Set Up RF Module**:
   - Connect NRF24L01 to Raspberry Pi SPI pins (e.g., CE to GPIO 8, CSN to GPIO 7).
   - Configure RF settings in `src/communication.py` (update `ALERT_APP_URL`).
5. **Power Configuration**:
   - Connect the battery pack to the motor driver.
   - Use a 5V regulator to power the Raspberry Pi.
   - Ensure all components share a common ground.

## Wiring Diagram
```
Raspberry Pi 4
├── GPIO 17 ---- L298N (Left Forward)
├── GPIO 27 ---- L298N (Left Backward)
├── GPIO 22 ---- L298N (Right Forward)
├── GPIO 23 ---- L298N (Right Backward)
├── GPIO 18 ---- L298N (Left Enable)
├── GPIO 24 ---- L298N (Right Enable)
├── GPIO 25 ---- HC-SR04 (Trigger)
├── GPIO 8  ---- HC-SR04 (Echo)
├── Camera Port ---- NoIR Camera
├── USB/Serial ---- RPLIDAR A1
├── UART (GPIO 14, 15) ---- NEO-6M GPS
├── SPI (GPIO 8, 7) ---- NRF24L01
```

## Notes
- Ensure proper insulation to prevent short circuits.
- Test each component individually using `scripts/test_hardware.py`.
- Update GPIO pin assignments in `src/config.py` if using different pins.
- Refer to component datasheets for detailed wiring instructions.