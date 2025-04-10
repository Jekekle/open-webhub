# Open WebUI Tunneling Options

This document explains how to expose your locally running Open WebUI instance to the internet using various tunneling services. This is useful for sharing your instance with others or accessing it from different devices without deploying to a public server.

## Available Tunneling Services

Open WebUI supports the following tunneling services:

1. **pyngrok** - A Python wrapper for ngrok, providing secure tunnels to localhost
2. **zrok** - An open-source alternative to ngrok with similar functionality
3. **pingy** - A simple tunneling service for exposing local servers

## Using the Tunneling Notebook

The easiest way to use tunneling with Open WebUI is to run the provided Jupyter notebook:

1. Open the `run_open_webui_with_tunnel.ipynb` notebook in Jupyter
2. Run through the cells to set up the environment
3. In the "Configure Tunneling" cell, choose your preferred tunneling service
4. Run the final cell to start the server with tunneling enabled

The notebook will display a public URL that you can use to access your Open WebUI instance from anywhere.

## Manual Configuration

If you prefer to set up tunneling manually, you can use the following environment variables:

```bash
# Enable tunneling
export WEBUI_ENABLE_TUNNEL=true

# Choose the tunneling service (pyngrok, zrok, or pingy)
export WEBUI_TUNNEL_SERVICE=pyngrok

# For pyngrok, you can set your ngrok auth token (optional)
export NGROK_AUTH_TOKEN=your_auth_token
```

Then start Open WebUI as usual.

## Service-Specific Notes

### pyngrok (Default)

- Automatically installed when needed
- For extended usage limits, set your ngrok auth token with `NGROK_AUTH_TOKEN`
- Most reliable option with good performance

### zrok

- Must be installed manually from [zrok.io](https://zrok.io/)
- Open-source alternative to ngrok
- No account required for basic usage

### pingy

- Automatically installed when needed
- Simple and lightweight
- Good for quick sharing

## Troubleshooting

- If the tunnel fails to establish, try restarting the server
- Check that the required service is properly installed
- For pyngrok, consider setting up an ngrok account and using your auth token
- Make sure your firewall isn't blocking the tunneling service
- If one service doesn't work, try another one

## Security Considerations

When using tunneling services, your Open WebUI instance becomes accessible from the internet. Consider the following security precautions:

1. Always set up proper authentication in Open WebUI
2. Use tunneling only when needed
3. Stop the tunnel when you're done using it
4. Be aware that free tunneling services may have limitations and potential security implications

## Why Not ngrok Directly?

While ngrok is a popular tunneling service, it has some limitations in its free tier and requires a separate installation. The solutions provided here offer more flexibility and better integration with Open WebUI.