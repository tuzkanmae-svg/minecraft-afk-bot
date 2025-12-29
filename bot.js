const mineflayer = require('mineflayer');

const serverHost = process.env.MC_SERVER_HOST || 'localhost';
const serverPort = process.env.MC_SERVER_PORT || 25565;
const username = process.env.MC_USERNAME || 'AFK_Bot';

console.log('==================================================');
console.log('Minecraft AFK Bot - 24/7 Server Keep Alive');
console.log('==================================================');
console.log(`Server: ${serverHost}:${serverPort}`);
console.log(`Bot Username: ${username}`);
console.log('==================================================');

function createBot() {
  const bot = mineflayer.createBot({
    host: serverHost,
    port: serverPort,
    username: username,
    version: '1.20.1' // Change cette version si nécessaire
  });

  bot.on('login', () => {
    console.log('[BOT] Bot connecté avec succès!');
    console.log(`[BOT] Vous êtes connecté en tant que: ${bot.username}`);
  });

  bot.on('spawn', () => {
    console.log('[BOT] Bot a spawn sur le serveur!');
    console.log('[BOT] Bot reste AFK...');
  });

  bot.on('error', (error) => {
    console.error('[BOT] Erreur:', error);
  });

  bot.on('kicked', (reason) => => {
    console.log('[BOT] Bot kické:', reason);
    console.log('[BOT] Reconnexion dans 5 secondes...');
    setTimeout(createBot, 5000);
  });

  bot.on('end', () => {
    console.log('[BOT] Connexion fermée. Reconnexion dans 5 secondes...');
    setTimeout(createBot, 5000);
  });
}

createBot();
