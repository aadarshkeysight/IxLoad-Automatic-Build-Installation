from logger import *
from controller import *

logger = get_logger(__name__)

def main():
    """Main entry point of the controller script."""
    setup_logger()
    print("Welcome to the IxLoad Controller\n")

    try:
        action = input("Select action (install/uninstall): ").strip().lower()

        if action == "install":
            perform_installation()
        elif action == "uninstall":
            perform_uninstallation()
        else:
            logger.error(f"Invalid action: '{action}'")
            print("Invalid action. Please choose 'install' or 'uninstall'.")

    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting...")
        logger.info("User interrupted the operation.")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"[Unexpected Error] {e}")


if __name__ == "__main__":
    main()
