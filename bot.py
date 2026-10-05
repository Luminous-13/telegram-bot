import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Render Web Service အတွက် HTTP Server ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# --- Telegram Bot Code ---
TOKEN = "8917617373:AAGJSuFAtfAROKjTs2JDfkBr-CTSgSuKCC8"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    numbers = re.findall(r'\d+', text)
    
    # စာထဲမှာ နံပါတ်ပါမှသာ တုံ့ပြန်မည်
    if numbers:
        found_numbers = " ".join(numbers)
        reply_text = f"<code>{found_numbers}</code>"
        
        keyboard = [
            [
                InlineKeyboardButton(
                    text="📋 Copy 🤍",
                    switch_inline_query_current_chat=found_numbers
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=reply_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    # နံပါတ်မပါပါက else အပိုင်းမပါတော့သဖြင့် Bot မှ ဘာမှ ပြန်မပို့တော့ပါ

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
