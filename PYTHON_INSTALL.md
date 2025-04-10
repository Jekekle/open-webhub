# Python-Only Installation for Open WebUI

This guide explains how to install and run Open WebUI using Python without Docker. This method is useful for users who prefer not to use Docker or need to run Open WebUI in environments where Docker is not available.

## Prerequisites

- Python 3.11 (required for compatibility with Open WebUI)
- Git (to clone the repository if you haven't already)

## Installation

1. Clone the Open WebUI repository (if you haven't already):
   ```bash
   git clone https://github.com/open-webui/open-webui.git
   cd open-webui
   ```

2. Install dependencies using the provided script:
   ```bash
   python install_and_run.py --install
   ```

## Running Open WebUI

### Basic Usage

To start Open WebUI with default settings (accessible at http://127.0.0.1:8080):

```bash
python install_and_run.py
```

### Advanced Options

The script supports several command-line options:

- `--host`: Specify the host to bind the server to (default: 127.0.0.1)
- `--port`: Specify the port to bind the server to (default: 8080)
- `--tunnel`: Enable tunneling to expose the server to the internet
- `--tunnel-service`: Choose the tunneling service (pyngrok, zrok, or pingy)
- `--ngrok-token`: Provide your ngrok auth token (only used with pyngrok)

### Examples

1. Run on a different port:
   ```bash
   python install_and_run.py --port 8000
   ```

2. Make the server accessible from other devices on your network:
   ```bash
   python install_and_run.py --host 0.0.0.0
   ```

3. Enable tunneling with pyngrok (default):
   ```bash
   python install_and_run.py --tunnel
   ```

4. Enable tunneling with a specific service and ngrok token:
   ```bash
   python install_and_run.py --tunnel --tunnel-service pyngrok --ngrok-token your_ngrok_token
   ```

## Tunneling Options

Open WebUI supports the following tunneling services:

1. **pyngrok** (default) - A Python wrapper for ngrok, providing secure tunnels to localhost
   - For extended usage limits, set your ngrok auth token with `--ngrok-token`
   - Most reliable option with good performance

2. **zrok** - An open-source alternative to ngrok with similar functionality
   - Must be installed manually from [zrok.io](https://zrok.io/)
   - Open-source alternative to ngrok
   - No account required for basic usage

3. **pingy** - A simple tunneling service for exposing local servers
   - Automatically installed when needed
   - Simple and lightweight
   - Good for quick sharing

## Troubleshooting

If you encounter any issues, here are some common troubleshooting steps:

1. **Port already in use**: If port 8080 is already in use, change the port using the `--port` option.

2. **Missing dependencies**: If you encounter missing dependencies, try running the script with the `--install` flag again.

3. **Database errors**: Open WebUI uses SQLite by default. Make sure the `backend/data` directory exists and is writable.

4. **Python version**: Make sure you're using Python 3.11 as required by Open WebUI.

5. **Path issues**: Make sure you're running the script from the Open WebUI root directory.

6. **Tunneling issues**: If tunneling fails, try a different tunneling service or check your firewall settings.

## Security Considerations

When using tunneling services, your Open WebUI instance becomes accessible from the internet. Consider the following security precautions:

1. Always set up proper authentication in Open WebUI
2. Use tunneling only when needed
3. Stop the server when you're done using it
4. Be aware that free tunneling services may have limitations and potential security implications