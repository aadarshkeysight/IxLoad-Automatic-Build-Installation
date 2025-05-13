import re
from logger import *
from cm_api import *
from api_client import *

logger = get_logger(__name__)

# Constants
VERSION_REGEX = r"^\d+\.\d+\.\d+\.\d+$"

def validate_input(prompt, validation_fn, error_message):
    """Prompt and validate user input using the provided validation function."""
    while True:
        user_input = input(prompt).strip()
        if validation_fn(user_input):
            return user_input
        logger.error(error_message)
        print(error_message)


def validate_build_version(version):
    """Check if the version matches format like 10.70.115.60."""
    return bool(re.match(VERSION_REGEX, version))


def validate_non_empty(value):
    """Ensure input is non-empty."""
    return bool(value.strip())


def perform_installation():
    """Run installation workflow."""
    pkgget_name = validate_input(
        "Enter pkgget name (e.g., ixload_apps): ",
        validate_non_empty,
        "Pkgget name cannot be empty."
    )

    build_version = validate_input(
        "Enter build version (e.g., 10.70.115.60): ",
        validate_build_version,
        "Invalid build version format."
    )

    #  local_path = validate_input(
    #     "Enter full path where IxLoad must be installed: ",
    #     validate_non_empty,
    #     "Installation path cannot be empty or invalid."
    # )

    build_location = find_build_location(pkgget_name, build_version)

    if not build_location:
        error_msg = f"Build location for {pkgget_name} version {build_version} not found."
        logger.error(error_msg)
        print(f"{error_msg} Exiting.")
        return

    logger.info(f"Installing build {build_version} from {build_location}")
    send_install_command(build_location, build_version)


def perform_uninstallation():
    """Run uninstallation workflow."""
    build_version = validate_input(
        "Enter build version to uninstall (e.g., 10.70.115.60): ",
        validate_build_version,
        "Invalid build version format."
    )

    # uninstall_path = validate_input(
    #     "Enter full uninstall path: ",
    #     validate_non_empty,
    #     "Uninstallation path cannot be empty or invalid."
    # )

    logger.info(f"Uninstalling build version {build_version}")
    send_uninstall_command(build_version)





