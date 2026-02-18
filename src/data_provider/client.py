from src.config.config import GETBLOCK_BCH_URL, GETBLOCK_BCH_API_KEY
import requests, json, time

_INTER_CALL_DELAY = 0.2

_MAX_RETRIES = 5
_BACKOFF_BASE = 2

def call_rpc(method, params=None):
    if params is None:
        params = []

    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    url = GETBLOCK_BCH_URL + GETBLOCK_BCH_API_KEY

    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            time.sleep(_INTER_CALL_DELAY)
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code != 200:
                raise Exception("Error in RPC call: " + str(response.text))
            return response.json().get('result', {})
        except Exception as e:
            last_error = e
            if attempt < _MAX_RETRIES:
                wait = _BACKOFF_BASE ** (attempt - 1)   # 1s, 2s, 4s, 8s …
                print(f"  [RPC] {method} failed (attempt {attempt}/{_MAX_RETRIES}), retrying in {wait}s… ({e})")
                time.sleep(wait)

    raise Exception(f"RPC call '{method}' failed after {_MAX_RETRIES} attempts: {last_error}")


# Strip 'bitcoincash:' prefix 
def _normalize_address(addr):
    if addr and addr.startswith('bitcoincash:'):
        return addr[len('bitcoincash:'):]
    return addr

# Check if address matches any in the list, ignoring bitcoincash: prefix
def _address_matches(address, addr_list):
    norm = _normalize_address(address)
    return any(_normalize_address(a) == norm for a in addr_list)


def get_address_activity(address, blocks_number):
    activity = []
    tx_cache = {}   
    height = call_rpc('getblockcount')
    
    print(f"Scanning blocks {height} to {height - blocks_number + 1}...")

    for i in range(height, height - blocks_number, -1):
        block_hash = call_rpc('getblockhash', [i])
        block = call_rpc('getblock', [block_hash, 2])
        txs = block['tx']
        
        print(f"  Block {i}: contain {len(txs)} txs")

        for tx in txs:
            txid = tx['txid']

            # Check outputs (received)
            for vout in tx['vout']:
                spk = vout.get('scriptPubKey', {})
                addrs = spk.get('addresses', [])
                if addrs and _address_matches(address, addrs):
                    activity.append({
                        'block_height': i,
                        'txid': txid,
                        'address': address,
                        'amount': vout['value'],
                        'type': 'received'
                    })

            # Check inputs (sent)
            for vin in tx['vin']:
                if 'coinbase' in vin:
                    continue

                prev_txid = vin.get('txid')
                prev_vout_idx = vin.get('vout')
                if prev_txid is None or prev_vout_idx is None:
                    continue

                if prev_txid not in tx_cache:
                    tx_cache[prev_txid] = call_rpc('getrawtransaction', [prev_txid, True])
                
                prev_tx = tx_cache[prev_txid]
                if not prev_tx or 'vout' not in prev_tx:
                    continue

                prev_vout = prev_tx['vout'][prev_vout_idx]
                prev_addrs = prev_vout.get('scriptPubKey', {}).get('addresses', [])

                if prev_addrs and _address_matches(address, prev_addrs):
                    sent_amount = sum(
                        v['value'] for v in tx['vout']
                        if not _address_matches(address, v.get('scriptPubKey', {}).get('addresses', []))
                    )
                    activity.append({
                        'block_height': i,
                        'txid': txid,
                        'address': address,
                        'amount': sent_amount,
                        'type': 'sent'
                    })
                    break 

    return activity
