# BCH Tracker

Bitcoin Cash (BCH) blockchain scanner that tracks address activity.

## Features

- **Scan the BCH blockchain** block by block via JSON-RPC (GetBlock or your own full node)
- Detect **received** and **sent** transactions for any address
- Handles the `bitcoincash:` address prefix automatically
- RPC response **caching** to minimize API calls
- Automatic retry with exponential backoff on RPC failures
- **SQLite database** integration to store and retrieve data
- **Statistics** of balance, sent/received totals, tx averages, activity per block

## Project Structure

```
BCH-tracker/
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
└── src/
    ├── config/
    │   ├── config.py              # YOUR API keys go here (gitignored)
    │   └── config_template.py     # Template — copy to config.py
    ├── data_provider/
    │   └── client.py              # JSON-RPC client & address scanner
    ├── database/
    │   ├── database.py            # DB init & schema
    │   └── database_handler.py    # DB read/write handlers
    └── statistics/
        └── scanner.py             # Stats computed from the DB
```

## Setup

```bash
# Clone the repo
git clone https://github.com/nilsecc/BCH-tracker.git
cd BCH-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # bash/zsh
# source venv/bin/activate.fish  # fish shell

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp src/config/config_template.py src/config/config.py
# Edit src/config/config.py and add your GetBlock API key
```

## Usage

```bash
python main.py
```

Enter your BCH address and the number of recent blocks to scan:

```
Address to check: qr...
Blocks to check: 5
Scanning blocks 938931 to 938927...
  Block 938931: contain 49 txs
  ...
Block 938931 | RECEIVED | 0.05000000 BCH | TXID: 96cd0ff3...

── Address summary: qr...
   Total received : 0.05000000 BCH
   Total sent     : 0.00000000 BCH
   Net balance    : 0.05000000 BCH
   Spent ratio    : 0.0%
   Transactions   : 1

── Received tx stats (1 txs)
   Max    : 0.05000000 BCH
   Min    : 0.05000000 BCH
   Avg    : 0.05000000 BCH

── Activity by block
   Block 938931: 1 tx(s)
```

## API Key

This project temporarily uses [GetBlock](https://getblock.io/) as the RPC provider. You can also point it at your own BCH full node, or any other provider.

1. Create an account at [getblock.io](https://getblock.io/)
2. Get your BCH mainnet endpoint + API key
3. Add it to `src/config/config.py`

## Roadmap

- [x] JSON-RPC client
- [x] Address activity scanner (received + sent)
- [x] SQLite database storage
- [x] Transaction statistics & analytics
- [ ] Full node support
- [ ] Extend data to include more details about transactions
- [ ] Add more complex statistics
- [ ] Terminal dashboard

This project is a work in progress. The main goal is to create a tool that can be used to track the activity of any address using a full node + indexer. This make the data getting process faster and more reliable.
