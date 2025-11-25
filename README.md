# Monzo Joint Spending Exporter

A Python-based tool for fetching Monzo transactions from your joint account, processing them into structured DataFrames, and exporting them to Excel with helpful formatting.
This project includes:
- OAuth2 authentication
- SQLite token persistence
- DataFrame processing
- Excel export
- Dev Container environment for development

## Features
### Current Functionality
- OAuth2 authentication via Monzo API
- Automatic extraction of tokens from redirect URLs
- Local SQLite DB for persistent token storage
- Token handler that auto-refreshes access tokens
- Fetch account list and recent transactions
- Convert transaction data → DataFrame
- Export to Excel with auto-width and centred text formatting
- Modular file structure: main.py, helper.py, db.py
- Full type annotations

### Development Environment
This project was developed using a VS Code Dev Container, allowing the user to run everything inside an isolated and consistent development environment.
The Dev container includes: 
- Python runtime environment
- Docker-in-Docker support
- Git Graph (VS Code extension)
- Draw.io (VS Code extension)
- Automatically activated Python virtual environment (venv)

## Built with:
- Python 3.10
- Monzo-API
- Pandas
- Openpyxl
- SQLite3
- Dotenv
- Dev Containers

## Environment Variables
Create a .env file with:
- CLIENT_ID=`<your monzo client id>`
- CLIENT_SECRET=`<your monzo client secret>`
- REDIRECT_URI=`<your monzo redirect uri>`

The Monzo-API provides a guide on how to generate credentials for your Monzo account. The guide can be found [here](https://monzo-api.readthedocs.io/en/latest/monzo_setup.html#creating-a-client).

## Excel Output
The Excel export of your joint spending will include the following:
- Date
- Merchant
- Amount (£)
- Category
- Cumulative Amount (£)
- Auto-sized columns
- Centred text

## Contributing
Any contributions are welcome!
