from src.data_provider.client import get_address_activity
from src.database.database import init_db
from src.database import database_handler as db
from src.statistics import scanner

if __name__ == "__main__":
    init_db()
    address_to_check = input("Address to check: ")
    blocks_to_check = int(input("Blocks to check: "))

    try:
        activity = get_address_activity(address_to_check, blocks_to_check)
        db.insert_activity(activity, address_to_check, blocks_to_check)
        scanner.print_all(address_to_check)

    except Exception as e:
        print(f"Error: {e}")
    
    
