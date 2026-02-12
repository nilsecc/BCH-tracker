from src.api.client import get_address_activity

if __name__ == "__main__":
    address_to_check = input("Address to check: ")
    blocks_to_check = int(input("Blocks to check: "))
    
    try:
        activity = get_address_activity(address_to_check, blocks_to_check)
        if not activity:
            print("No activity found in the checked blocks.")
        for entry in activity:
            print(f"Block Height: {entry['block_height']}, TXID: {entry['txid']}, Type: {entry['type']}, Amount: {entry['amount']}")
    except Exception as e:
        print(f"Error: {e}")
