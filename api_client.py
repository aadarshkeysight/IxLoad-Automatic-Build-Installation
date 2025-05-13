import requests
import threading
from logger import *
from config import AGENT_IP, AGENT_PORT
import time

logger = get_logger(__name__)

i = 1
# Function to listen to progress
def listen_to_progress():
    link = f"http://{AGENT_IP}:{AGENT_PORT}/progress"
    while i != 0: 
        with requests.get(link, stream=True) as response:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(f"[Progress] {line}")
        time.sleep(5)


def send_install_command(build_info, build_version):
    """Send the install command to the agent."""
    url = f"http://{AGENT_IP}:{AGENT_PORT}/download"
    
    # Parse the network path
    network_path = build_info['path']
    cleaned_path = network_path.lstrip('\\')
    server, *remote_parts = cleaned_path.split('\\')
    remote_dir = '/'.join(remote_parts + ['Disk1'])

    # Prepare payload for agent
    payload = {
        "ixload_ver": build_version,
        "path": server,
        "remote_dir": remote_dir,
    }

    headers = {'Content-type': 'application/json'}

    stop_event = threading.Event()

    # # Start the listener in a separate thread for progress streaming
    # listener_thread = threading.Thread(
    #     target=listen_to_progress, args=(stop_event,)
    # )
    # listener_thread.start()

    listener_thread = threading.Thread(target=listen_to_progress)
    listener_thread.start()

    # Send POST request to install endpoint
    try:
        logger.info(f"Sending install command to {url} with payload: {payload}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"Install command successful: {response.text}")
        else:
            logger.error(f"Unexpected response status: {response.status_code}, {response.text}")
        
    except requests.RequestException as e:
        logger.error(f"Failed to send install command: {e}")
    finally:
        # stop_event.set() 
        global i
        i = 0
        listener_thread.join()


def send_uninstall_command(build_version):
    """Send the uninstall command to the agent."""
    url = f"http://{AGENT_IP}:{AGENT_PORT}/uninstall"
    payload = {
        # "uninstall_path": uninstall_path,
        "ixload_ver": build_version
    }

    # stop_event = threading.Event()

    # listener_thread = threading.Thread(
    #     target=listen_to_progress, args=(stop_event,)
    # )
    # listener_thread.start()

    listener_thread = threading.Thread(target=listen_to_progress)
    listener_thread.start()

    # Send POST request to uninstall endpoint
    try:
        logger.info(f"Sending uninstall command to {url} with payload: {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()

        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"Uninstall command successful: {response.text}")
        else:
            logger.error(f"Unexpected response status: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        logger.error(f"Failed to send uninstall command: {e}")
    finally:
        # stop_event.set() 
        global i
        i = 0
        listener_thread.join()
