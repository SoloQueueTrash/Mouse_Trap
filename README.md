# Mouse Trap

| Name          | Number        | E-Mail               |
|---------------|---------------|----------------------|
| Isaac Silva   | up201907420 | up201907420@fc.up.pt |
| Nuno Domingos | up201907932   | up201907932@fc.up.pt |
| Pedro Santos  | up201904529   | up201904529@fc.up.pt |
| Tomás Vicente | up201904609   | up201904609@fe.up.pt |

# Automatic Mousetrap System

## Overview
The project aimed to develop an automatic mousetrap system that detects movement inside the trap, captures photographs, and allows users to remotely control the trap via a mobile application. The system was designed to close the trap door automatically after 5 seconds of detecting movement or sooner, depending on the user's decision through the app.

## Components

### 1. **Physical Mousetrap**
- **Structure:** Built with a wooden base and metal mesh to allow light entry for photo capture.
- **Key Components:**
  - **Servo Motor:** Controls the door mechanism.
  - **PIR Motion Sensor:** Detects movement inside the trap.
  - **Arduino Uno:** Acts as the microcontroller, controlling the door and processing sensor data.
  - **Raspberry Pi:** Acts as the server, connected to a camera module for capturing images. It communicates with the Arduino and the mobile application.

### 2. **Arduino**
- **Functionality:**
  - Controls the trap door.
  - Detects movement using the PIR sensor.
  - Sends movement detection information to the Raspberry Pi.
  - Executes a state machine that handles door operations based on movement detection and commands from the server.

### 3. **Raspberry Pi**
- **Role:**
  - Serves as the main server, executing Python code.
  - Manages communication between the Arduino and the mobile application.
  - Handles requests to capture and store photographs using the connected camera module.
  - Uses serial communication to interact with the Arduino and HTTP requests to communicate with the mobile app.

### 4. **Mobile Application**
- **Platform:** Developed using Google’s Flutter framework for cross-platform compatibility (Android, iOS, etc.).
- **Features:**
  - Users can monitor the state of multiple traps.
  - Users can remotely control the trap door and request new photographs.
  - Notifications alert users of movement inside the trap, including a photograph and door status.

## Integration
The integration process involved connecting the sensor and servo motor to the Arduino and ensuring correct communication between the Arduino and Raspberry Pi via a physical serial connection. The mobile application interacted with the Raspberry Pi through HTTP requests, facilitating remote control and monitoring.

## Challenges and Solutions

### 1. **Constant Data Reading**
- **Problem:** The server needed to constantly monitor communication between the Arduino and Raspberry Pi, which is atypical for a standard HTTP server.
- **Solution:** Implemented a background thread in the server that continuously listens for messages from the Arduino, such as movement detection, and triggers appropriate actions like sending notifications to the mobile application.

### 2. **PIR Sensor Sensitivity**
- **Problem:** The PIR sensor was overly sensitive, leading to false positives, and required an initial setup time to stabilize.
- **Solution:** Introduced a 20-second setup time for the PIR sensor during which the trap remains inactive. This allowed the sensor to adjust to the environment, reducing false detections.

### 3. **General Development Issues**
- **Problem:** Encountered various dependency issues and unexpected behaviors during development.
- **Solution:** These issues were swiftly identified and resolved, ensuring they did not significantly impact the project's progress.

## Conclusion
The project successfully created a functional and responsive automatic mousetrap system, integrating various hardware and software components. Despite the challenges faced during development, appropriate solutions were implemented, resulting in a versatile system that allows users to remotely monitor and control the mousetraps efficiently via a mobile application.
