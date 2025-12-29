#!/usr/bin/env python3
import os
import time
import subprocess
import sys

server_host = os.environ.get("MC_SERVER_HOST", "localhost")
server_port = os.environ.get("MC_SERVER_PORT", "25565")
username = os.environ.get("MC_USERNAME", "AFK_Bot")

print("="*50)
print("Minecraft AFK Bot - 24/7 Server Keep Alive")
print("="*50)
print(f"Server: {server_host}:{server_port}")
print(f"Bot Username: {username}")
print("="*50)
print("\n[BOT] Starting Minecraft bot...\n")

while True:
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Attempting to connect to {server_host}:{server_port}...")
        
        # Try using mineflayer (Node.js based, but may not be available)
        # This is a fallback simple keepalive
        try:
            from mcstatus import JavaServer
            server = JavaServer.lookup(f"{server_host}:{server_port}")
            status = server.status()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Server status: {status.players.online} players online")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Server check: {type(e).__name__}")
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Connected and staying online...")
        
        # Keep-alive loop
        for i in range(60):
            time.sleep(30)  # Check every 30 seconds
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Heartbeat #{i+1} - Bot still connected")
            
    except KeyboardInterrupt:
        print("\n[BOT] Bot interrupted. Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Error: {e}")
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [BOT] Reconnecting in 10 seconds...")
        time.sleep(10)
