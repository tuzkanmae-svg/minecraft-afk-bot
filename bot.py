#!/usr/bin/env python3
import os
import time
import logging
from minecraft.authentication import AuthenticationException, InvalidCredentialsException
from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import chat_type

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinecraftAFKBot:
    def __init__(self, server_host, server_port=25565, username="AFK_Bot", use_offline_mode=True):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.use_offline_mode = use_offline_mode
        self.connection = None
        
    def connect(self):
        """Connect to the Minecraft server"""
        logger.info(f"[BOT] Attempting to connect to {self.server_host}:{self.server_port}")
        logger.info(f"[BOT] Username: {self.username}")
        
        try:
            self.connection = Connection(
                self.server_host,
                self.server_port,
                username=self.username,
                auth_token=None if self.use_offline_mode else None
            )
            self.connection.connect()
            logger.info(f"[BOT] Successfully connected to {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Connection failed: {e}")
            return False
    
    def stay_connected(self):
        """Keep the bot connected and send periodic keepalive packets"""
        logger.info("[BOT] Staying connected... (AFK mode)")
        
        try:
            while self.connection and self.connection.network_thread.is_alive():
                time.sleep(30)
                logger.info(f"[BOT] Still connected at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except KeyboardInterrupt:
            logger.info("[BOT] Shutting down...")
            if self.connection:
                self.connection.disconnect()
        except Exception as e:
            logger.error(f"[ERROR] {e}")
            if self.connection:
                self.connection.disconnect()
    
    def run(self):
        """Main bot loop"""
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            if self.connect():
                self.stay_connected()
                retry_count = 0
            else:
                retry_count += 1
                wait_time = min(2 ** retry_count, 300)
                logger.info(f"[BOT] Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)

if __name__ == "__main__":
    # Get configuration from environment variables
    server_host = os.environ.get("MC_SERVER_HOST", "localhost")
    server_port = int(os.environ.get("MC_SERVER_PORT", "25565"))
    username = os.environ.get("MC_BOT_USERNAME", "AFK_Bot")
    
    logger.info("=" * 50)
    logger.info("Minecraft AFK Bot - 24/7 Server Keep-Alive")
    logger.info("=" * 50)
    logger.info(f"Server: {server_host}:{server_port}")
    logger.info(f"Bot Username: {username}")
    logger.info("=" * 50)
    
    bot = MinecraftAFKBot(server_host, server_port, username)
    bot.run()
