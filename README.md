# BCH tracker

Bitcoin Cash (BCH) blockchain scanner that tracks address activity using the JSON-RPC API.

## Features
- Scan the BCH blockchain block by block via JSON-RPC (GetBlock or your own full node)
- Detect **received** and **sent** transactions for any address
- Handles the `bitcoincash:` address prefix automatically
- RPC response caching to minimize API calls

## Pending features
- [ ] Add database support
- [ ] Add block analysis logic
- [ ] Add terminal dashboard with statistics

## Project Structure

```
BCH-tracker/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── src/
│   ├── api/
│   │   └── client.py          # JSON-RPC client & address scanner
│   ├── config/
│   │   ├── config.py          # YOUR API keys (gitignored)
│   │   └── config.example.py  # Template for config.py
│   ├── core/
│   │   └── scanner.py         # Block analysis logic (not done yet)
│   └── database/
│       └── manager.py         # DB storage (not done yet)
```

## Setup

```bash
# Clone the repo
git clone https://github.com/nilsecc/BCH-tracker.git
cd BCH-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
# if using fish: source venv/bin/activate.fish

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp src/config/config.example.py src/config/config.py
# Or directly edit src/config/config.py and add your GetBlock API key
```

## Usage

Edit `main.py` to set the target address and number of blocks to scan:

```python
address_to_check = "qqw5tr9x8t73uqes53jewjk7ks63tz3xmygq3k64x4"
blocks_to_check = 10
```

Run the scanner:

```bash
python main.py
```

Example output:

```
Scanning blocks 937980 to 937971...
  Block 937980: contain 134 txs
  Block 937979: contain 290 txs
  ...
Block Height: 937979, TXID: 96cd0ff3..., Type: received, Amount: 3.14260572
```

## API Key

This project temporarily uses [GetBlock](https://getblock.io/) as the RPC provider. You can also use your own BCH full node, or any other provider.

1. Create an account at [getblock.io](https://getblock.io/)
2. Get your BCH mainnet API key
3. Add it to `src/config/config.py`

## Roadmap

- [x] JSON-RPC client
- [x] Address activity scanner (received + sent)
- [ ] SQLite database storage
- [ ] Transaction statistics & analytics
- [ ] Terminal dashboard

