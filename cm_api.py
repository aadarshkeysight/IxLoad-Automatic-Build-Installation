import requests
import yaml
from config import CM_API_URL


def find_build_location(pkgget_name, build_version):
    """Find the build location based on preferred locations from the CM API."""
    try:
        # Prepare the payload for the request
        payload = {
            'product': pkgget_name,
            'build_no': build_version,
            'jsonFormat': 'True',
        }

        # Make the API request
        response = requests.post(CM_API_URL, data=payload)
        response.raise_for_status()

        # Parse the response JSON
        build_info = response.json()

        # Check if 'database' exists in the response
        if 'database' not in build_info:
            return None

        # Filter locations that contain both 'location' and 'path'
        locations = [
            {'location': entry['location'], 'path': entry['path']}
            for entry in build_info['database']
            if 'location' in entry and 'path' in entry
        ]

        if not locations:
            return None

        # Preferred locations
        preferred_order = ['Kolkata', 'Calabasas', 'Bucharest', 'S3']

        # Search locations based on preference
        for preferred_location in preferred_order:
            for loc in locations:
                if loc['location'].lower() == preferred_location.lower():
                    return {'location': loc['location'], 'path': loc['path']}  # Return the build location with path

        return None  

    except requests.exceptions.RequestException:
        return None
    except ValueError:
        return None
    except Exception:
        return None
