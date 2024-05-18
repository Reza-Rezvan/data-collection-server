# Data Collection Server
A Flask-based server for collecting and displaying hardware data.

## Overview
This project sets up a server using Flask to collect data from various hardware devices, store it in a SQLite database, and display the data in a web interface. The data includes information such as hardware ID, timestamps, speed, labels, and image data.

## Features
- Collects data from hardware devices.
- Stores data in a SQLite database.
- Displays collected data in a web interface.
- Provides download links for images.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Reza-Rezvan/data-collection-server.git
    cd data-collection-server
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Create database.db on server:**
    - use the `create.py` scripts to create `database.db` on server
1. **Run the Flask Server:**
    ```sh
    python server.py
    ```

2. **Generate and Send Data:**
    - Use the `send_data.py` script to generate random data and send it to the server.
    

3. **Access the Web Interface:**
    Open a web browser and navigate to `http://<server-ip>:1234/hardware` to view the collected data.

## File Structure
- `create.py`: Script to create the SQLite database and tables.
- `send_data.py`: Script to generate and send random data with images.
- `server.py`: The main Flask server application.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
