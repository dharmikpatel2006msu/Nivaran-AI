const { Bot } = require('node-telegram-bot-api');
require('dotenv').config();

const bot = new Bot(process.env.TELEGRAM_BOT_TOKEN);

bot.command('start', (ctx) => {
  console.log('HANDLED /start');
});

bot.on('message:text', (ctx) => {
  console.log('HANDLED message:text ->', ctx.message.text);
});

bot.on('message', (ctx) => {
  console.log('HANDLED message ->', ctx.message.text);
});

(async () => {
  console.log('Simulating /start update...');
  await bot.handleUpdate({
    update_id: 1,
    message: { message_id: 1, date: 100, chat: { id: 123, type: 'private' }, text: '/start', from: { id: 123, first_name: 'Test' } }
  });

  console.log('Simulating text update...');
  await bot.handleUpdate({
    update_id: 2,
    message: { message_id: 2, date: 100, chat: { id: 123, type: 'private' }, text: 'What are your store hours?', from: { id: 123, first_name: 'Test' } }
  });
})();
