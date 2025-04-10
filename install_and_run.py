#!/usr/bin/env python3

import argparse
import os
import platform
import secrets
import subprocess
import sys
import time
from pathlib import Path

# Check Python version
if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
    print("WARNING: Open WebUI requires Python 3.11. You may encounter compatibility issues.")

# Get the current directory
CURRENT_DIR = Path.cwd()
BACKEND_DIR = CURRENT_DIR / 'backend'
REQUIREMENTS_FILE = BACKEND_DIR / 'requirements.txt'

def check_dependencies():
    """Check if all required dependencies are installed"""
    if not REQUIREMENTS_FILE.exists():
        print(f"Error: {REQUIREMENTS_FILE} not found. Make sure you're running this script from the Open WebUI root directory.")
        sys.exit(1)

def install_dependencies():
    """Install all required dependencies"""
    print(f"Installing dependencies from {REQUIREMENTS_FILE}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(REQUIREMENTS_FILE)])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_environment(host, port, enable_tunnel, tunnel_service, ngrok_token=None):
    """Set up environment variables for Open WebUI"""
    # Set basic environment variables
    os.environ['HOST'] = host
    os.environ['PORT'] = str(port)
    
    # Generate a random secret key if not already set
    if 'WEBUI_SECRET_KEY' not in os.environ:
        os.environ['WEBUI_SECRET_KEY'] = secrets.token_hex(16)
        print(f"Generated WEBUI_SECRET_KEY: {os.environ['WEBUI_SECRET_KEY']}")
    
    # Set tunneling environment variables if enabled
    if enable_tunnel:
        os.environ['WEBUI_ENABLE_TUNNEL'] = 'true'
        os.environ['WEBUI_TUNNEL_SERVICE'] = tunnel_service
        
        if tunnel_service == 'pyngrok' and ngrok_token:
            os.environ['NGROK_AUTH_TOKEN'] = ngrok_token
            print(f"Using ngrok auth token: {ngrok_token}")
    
    print("Environment variables configured successfully!")

def start_server(host, port, enable_tunnel, tunnel_service):
    """Start the Open WebUI server"""
    # Add the backend directory to the Python path
    if str(BACKEND_DIR) not in sys.path:
        sys.path.append(str(BACKEND_DIR))
    
    # Change to the backend directory
    os.chdir(BACKEND_DIR)
    
    try:
        print("Starting Open WebUI server...")
        
        # Import required modules
        import uvicorn
        from open_webui.utils.tunneling import get_tunneling_service
        
        # Start tunneling if enabled
        tunnel_url = None
        if enable_tunnel:
            print(f"Setting up {tunnel_service} tunnel...")
            tunneling_service = get_tunneling_service(tunnel_service)
            tunnel_url = tunneling_service.start_tunnel(int(port))
            
            if tunnel_url:
                print(f"Tunnel established at: {tunnel_url}")
                print(f"You can access Open WebUI from anywhere using this URL")
            else:
                print(f"Failed to establish tunnel with {tunnel_service}. Continuing with local server only.")
        
        # Print access information
        print(f"Open WebUI will be available at http://{host}:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Start the server
        uvicorn.run(
            'open_webui.main:app',
            host=host,
            port=int(port),
            reload=False
        )
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        # Change back to the original directory
        os.chdir(CURRENT_DIR)

def main():
    parser = argparse.ArgumentParser(description='Install and run Open WebUI without Docker')
    parser.add_argument('--install', action='store_true', help='Install dependencies')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind the server to (default: 127.0.0.1)')
    parser.add_argument('--port', default='8080', help='Port to bind the server to (default: 8080)')
    parser.add_argument('--tunnel', action='store_true', help='Enable tunneling to expose the server to the internet')
    parser.add_argument('--tunnel-service', default='pyngrok', choices=['pyngrok', 'zrok', 'pingy'], 
                        help='Tunneling service to use (default: pyngrok)')
    parser.add_argument('--ngrok-token', help='Ngrok auth token (only used with pyngrok)')
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Install dependencies if requested
    if args.install:
        install_dependencies()
    
    # Set up environment
    setup_environment(args.host, args.port, args.tunnel, args.tunnel_service, args.ngrok_token)
    
    # Start the server
    start_server(args.host, args.port, args.tunnel, args.tunnel_service)

if __name__ == '__main__':
    main()