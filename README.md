<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# Monzo Joint Account Spending Exporter

<em>Export Shared Spending From Your Monzo Account</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/30carterjack/monzo-joint-spending-exporter?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/30carterjack/monzo-joint-spending-exporter?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/30carterjack/monzo-joint-spending-exporter?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the following tools:</em>

<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Dev Container](#devcontainer)
    - [Usage](#usage)
    - [Testing](#testing)

---

## Overview

Monzo Joint Account Spending Exporter is a small tool designed to securely retrieve, process, and export joint account transactions from Monzo into formatted Excel files. It simplifies financial data extraction, enabling greater understanding of shared spending.

**Why Monzo Joint Account Spending Exporter?**

This project simplifies the process of accessing and collating financial data from Monzo, supporting clearer analysis. The core features include:

- 🛠️ **Secure OAuth2 Authentication:** Manages tokens securely with persistent storage, ensuring reliable API access.
- 📊 **Data Export:** Converts raw transaction data into structured, visually formatted Excel reports.
- 🔧 **Utility Functions:** Facilitates cost normalization, user approval workflows, date handling, and token expiration checks.
- ⚙️ **Modular Design:** Supports easy integration, extension, and maintenance within larger systems.
- 🚀 **Automated Data Retrieval:** Fetches account details and recent transactions with minimal effort.
- 💾 **Persistent Token Management:** Ensures seamless, ongoing access to the user's financial data.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Monzo OAuth Client**: See next section

### Creating a Monzo Client
To use this tool, you’ll need to create a Monzo OAuth Client (Client ID, Client Secret, and Redirect URI).
This step is required before the application can authenticate with the Monzo API.
Full instructions are provided in the Monzo API documentation:

👉 https://monzo-api.readthedocs.io/en/latest/monzo_setup.html#creating-a-client

Make sure you follow that guide to set up your client before running the exporter.

### Installation

Build Monzo Joint Account Spending Exporter from the source and install dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/30carterjack/monzo-joint-spending-exporter
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd monzo-joint-spending-exporter
    ```

3. **Install the dependencies:**

**Using [pip](https://pypi.org/project/pip/):**

```sh
❯ pip install -r requirements.txt
```

### Development Environment

This project was developed using a VS Code Dev Container, allowing the user to run everything inside an isolated and standardised development environment.
The Dev container includes: 

- Python runtime environment
- Docker-in-Docker support
- Git Graph (VS Code extension)
- Draw.io (VS Code extension)
- Automatically activated Python virtual environment (venv)


### Usage

Run the project with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
python main.py
```

---

<div align="left"><a href="#top">⬆ Return</a></div>

---
