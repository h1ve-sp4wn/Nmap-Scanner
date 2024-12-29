To install the necessary Python libraries, you can run the following command:

    pip install nmap requests

External System Dependencies

The script relies on Nmap for advanced port scanning. You'll need to install Nmap on your system, which is a tool used for discovering hosts and services on a computer network.

Linux (Debian/Ubuntu-based systems):

    sudo apt install nmap

macOS:

    brew install nmap

Windows: Download the installer from the Nmap official site and install it.

Once you have Nmap installed, make sure it’s available in your system’s PATH. You can check it with:

    nmap --version

2. Running the Script in the Terminal

Step 1: Set Up Python Environment

Ensure Python 3.7 or higher is installed: You can check your Python version using:

    python3 --version

Set up a virtual environment (optional but recommended):

    python3 -m venv venv

    source venv/bin/activate  # On Linux/macOS

    .\venv\Scripts\activate   # On Windows

Install required Python libraries: Install nmap and requests using pip:

    pip install nmap requests

Install Nmap (if you haven’t already): Follow the instructions provided earlier for installing Nmap on your system.

Step 2: Run the Script

Navigate to the directory where your script is located, and execute it with:

    python3 nmap_scanner.py

To use it with Docker:

Build the Docker Image

In the same directory as your Dockerfile, run the following command to build the Docker image:

    docker build -t nmap-scanner .

This will build the Docker image and tag it as vulnerability-scanner.

Step 3: Run the Docker Container

Once the image is built, run the container using:

    docker run --rm nmap-scanner

--rm ensures that the container is removed after it finishes running.

You can replace vulnerability-scanner with your preferred image name if you chose something different.

Step 4: (Optional) Run the Container with Elevated Privileges

For the nmap command to work properly, it may need elevated privileges. You can use the --privileged flag to run the container with more access:

    docker run --rm --privileged nmap-scanner

4. Important Notes

Nmap & Privileges: In Docker, Nmap needs access to raw sockets for certain types of scans (e.g., -sS for stealth scans). Running the container with the --privileged flag gives it the necessary permissions to execute these scans.
   
Python AsyncIO: The script uses asyncio for asynchronous tasks like fetching banners from open ports. It should work out of the box if Python 3.7+ is installed.
