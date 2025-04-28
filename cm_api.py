import requests
from utils import log_info, log_error
import yaml

# Load the config
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

CM_API_URL = config['cm_api']['url']

def find_build_location(pkgget_name, build_version):
    try:
        payload = {
            'product': pkgget_name,
            'build_no': build_version,
            'jsonFormat': 'True',
        }

        # Make the API request
        response = requests.post(CM_API_URL, data=payload)
        response.raise_for_status()

        # Try to parse the response as JSON
        try:
            build_info = response.json()

            if 'database' not in build_info:
                log_error("No 'database' field found in CM API response.")
                return None

            locations = []
            for entry in build_info['database']:
                if 'location' in entry and 'path' in entry:
                    locations.append({
                        'location': entry['location'],
                        'path': entry['path']
                    })

            if not locations:
                log_error("No valid locations found in the CM response.")
                return None

            # Define preference order
            preferred_order = ['Kolkata', 'Calabasas', 'Bucharest']

            # Search based on preference
            for preferred_location in preferred_order:
                for loc in locations:
                    if loc['location'].lower() == preferred_location.lower():
                        log_info(f"Preferred build found at location: {loc['location']} with path: {loc['path']}")
                        return loc  # Immediately return first match

            # If no preferred location found
            log_error("Preferred locations (Kolkata, Calabasas, Bucharest) not found in CM response.")
            return None

        except ValueError:
            log_error(f"Error parsing JSON response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        log_error(f"Error contacting CM API: {str(e)}")
        return None

    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        return None
