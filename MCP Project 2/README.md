# Equity Trading System

A Python-based mini equity trading platform that allows users to:
- Create and manage trading accounts
- Deposit and withdraw funds
- Buy and sell stocks at live market prices (with spread)
- Track holdings, transaction history, profit & loss, and portfolio value

---

## Features

- **Account Management:** Create, reset, and manage trading accounts.
- **Fund Management:** Deposit and withdraw cash.
- **Stock Trading:** Buy and sell stocks with real-time pricing and realistic spread.
- **Portfolio Tracking:** View current holdings, transaction history, profit/loss, and total portfolio value.
- **Audit Logging:** All actions are logged for transparency.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd MCP Project 2
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
- If you use any API keys or database configs, create a `.env` file in the project root.
- Example `.env`:
  ```env
  API_KEY=your_api_key_here
  DB_PATH=your_database_path_here
  ```

### 4. Run the Sample Script
```bash
python equity_account.py
```

---

## Usage Example

```python
from equity_account import EquityAccount

# Create a new account
equity_account = EquityAccount('Alice')

# Deposit funds
equity_account.deposit_funds(1000)

# Buy stocks
equity_account.purchase_stock('AAPL', 5, 'Long-term investment')

# Sell stocks
equity_account.sell_stock('AAPL', 2, 'Taking profit')

# View holdings
print('Holdings:', equity_account.get_holdings())

# View transaction history
print('Transactions:', equity_account.equity_transactions_list())

# View portfolio value
print('Portfolio Value:', equity_account.calculate_equity_portfolio_value())

# View profit and loss
print('Profit & Loss:', equity_account.get_equity_profit_and_loss())
```

---

## Project Structure

```
MCP Project 2/
├── equity_account.py        # Main account and transaction logic
├── equity_market.py         # Market data fetching
├── equity_database.py       # Database and logging utilities
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variable management

---

## Contact

For questions or suggestions, please contact the project maintainer. 