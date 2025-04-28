import requests
from Scripts.utils import log_info, log_error
import yaml

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Extract agent IP and port from the config file
AGENT_IP = config['agent']['ip']
AGENT_PORT = config['agent']['port']


def stream_logs(response):
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
                log_info(decoded_line)
    except Exception as e:
        log_error(f"Error while streaming logs: {e}")
        
        
        
# Send install commadn to the agent
def send_install_command(build_info, build_version, local_path, silent_flags):
    
    url = f"http://{AGENT_IP}:{AGENT_PORT}/install"
    
    # Parse the network path
    network_path = build_info['path'] 
    cleaned_path = network_path.lstrip('\\')
    server, *remote_parts = cleaned_path.split('\\')
    remote_dir = '/'.join(remote_parts)

    # Prepare payload for agent
    payload = {
        "ixload_ver": build_version,
        "path": server,
        "remote_dir": remote_dir,
        "local_path": local_path,
        "silent_flags":silent_flags
    }
    
    # Send a post request to the agent's install endpoint
    try:
        log_info(f"Sending install command to {url} with payload : {payload}")
        response = requests.post(url, json=payload,timeout=30,stream=True)
        response.raise_for_status()
        
        # Checking if the response was successful
        if response.status_code == 200:
            log_info(f"Install command successful: {response.text}")
            stream_logs(response)
        else:
            log_error(f"Unexpected response status: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        log_error(f"Failed to send install command: {e}")
        
        
        
# Function to send an uninstall command to the agent
def send_uninstall_command(build_version,uninstall_path, silent_flags):
    url = f"http://{AGENT_IP}:{AGENT_PORT}/uninstall"
    payload = {
        "uninstall_path": uninstall_path,
        "silent_flags": silent_flags,
        "build_version": build_version
    }
    
    # Send a POST request with the payload to the agent's uninstall endpoint
    try:
        log_info(f"Sending uninstall command to {url} with payload: {payload}")
        response = requests.post(url, json=payload, timeout=30,stream=True)  
        response.raise_for_status()

        # Checking if the response was successful
        if response.status_code == 200:
            log_info(f"Uninstall command successful: {response.text}")
            stream_logs(response)
        else:
            log_error(f"Unexpected response status: {response.status_code}, {response.text}")
            
    except requests.RequestException as e:
        log_error(f"Failed to send uninstall command: {e}")
