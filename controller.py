from Scripts.utils import setup_logger, log_info, log_error
from Scripts.cm_api import find_build_location
from Scripts.api_client import send_install_command, send_uninstall_command

def main():
    # Setup the logger
    setup_logger()
    print("Welcome to the IxLoad Controller\n")

    # Prompt user to select an action
    action = input("Select Action (install/uninstall): ").strip().lower()

    # Validate the action
    if action not in ["install", "uninstall"]:
        print("Invalid action. Exiting.")
        return

    if action == "install":
        pkgget_name = input("Enter pkgget name (e.g., ixload_apps): ").strip()
        build_version = input("Enter build version (e.g., 10.70.115.60): ").strip()
        local_path = input("Enter full path where IxLoad must be installed ").strip()
        silent_flags = "-s i CannedConfig=Full AUTOREBOOT=No"

        # Find build location
        build_location = find_build_location(pkgget_name, build_version)

        if not build_location:
            print("Could not find build location. Exiting.")
            return

        
        send_install_command(build_location,build_version, local_path, silent_flags)

    else:  # uninstall
        build_version = input("Enter build version to uninstall (e.g., 10.70.115.60): ").strip()
        uninstall_path = input(
            "Enter full uninstall path (e.g., C:/Program Files (x86)/IxiaInstallerCache/IxLoad/10.70.115.60/setup.exe): "
        ).strip()

        silent_flags = "-s x AUTOREBOOT=No"
        send_uninstall_command(build_version,uninstall_path, silent_flags)

if __name__ == "__main__":
    main()
