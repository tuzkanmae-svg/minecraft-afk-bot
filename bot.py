#!/usr/bin/env python3
import os
import time
import logging
from minecraft.authentication import OfflineAuthentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import chat_type

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinecraftAFKBot:
    def __init__(self, server_host, server_port=25565, username="AFK_Bot"):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.connection = None

    def connect(self):
        """Connect to the Minecraft server"""
        logger.info(f"[BOT] Attempting to connect to {self.server_host}:{self.server_port}")
        logger.info(f"[BOT] Username: {self.username}")

        try:
            # Use offline authentication mode
            auth = OfflineAuthentication(username=self.username)
            self.connection = Connection(
                self.server_host,
                self.server_port,
                auth_token=None,
                username=self.username
            )
            
            self.connection.connect()
            logger.info(f"[BOT] Successfully connected to {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Connection failed: {e}")
            return False

    def stay_connected(self):
        """Keep the bot connected and respond to keep-alive packets"""
        logger.info("[BOT] Entering keep-alive loop...")
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Read packets and respond to keep-alives
                while self.connection and self.connection.network_thread.is_alive():
                    time.sleep(30)  # Check every 30 seconds
                    logger.info(f"[BOT] Still connected at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # If we're here, connection died
                if retry_count < max_retries - 1:
                    logger.warning(f"[BOT] Connection lost. Reconnecting... (Attempt {retry_count + 1}/{max_retries})")
                    retry_count += 1
                    time.sleep(10 + retry_count * 5)  # Exponential backoff
                    if not self.connect():
                        continue
                    logger.info("[BOT] Reconnected successfully!")
                else:
                    logger.error("[BOT] Max retries reached. Shutting down...")
                    break
                    
            except KeyboardInterrupt:
                logger.info("[BOT] Interrupted by user.")
                break
            except Exception as e:
                logger.error(f"[ERROR] Unexpected error: {e}")
                if retry_count < max_retries - 1:
                    retry_count += 1
                    time.sleep(10)
                else:
                    break

    def disconnect(self):
        """Disconnect from the server"""
        if self.connection:
            try:
                self.connection.disconnect()
                logger.info("[BOT] Disconnected.")
            except Exception as e:
                logger.error(f"[ERROR] Error during disconnect: {e}")

if __name__ == "__main__":
    # Get configuration from environment variables
    server_host = os.environ.get("MC_SERVER_HOST", "localhost")
    server_port = int(os.environ.get("MC_SERVER_PORT", "25565"))
    username = os.environ.get("MC_USERNAME", "AFK_Bot")
    
    logger.info("="  * 50)
    logger.info("Minecraft AFK Bot - 24/7 Server Keep Alive")
    logger.info("="  * 50)
    logger.info(f"Server: {server_host}:{server_port}")
    logger.info(f"Bot Username: {username}")
    logger.info("="  * 50)
    
    bot = MinecraftAFKBot(server_host, server_port, username)
    
    try:
        if bot.connect():
            bot.stay_connected()
        else:
            logger.error("[BOT] Failed to connect initially.")
    finally:
        bot.disconnect()
