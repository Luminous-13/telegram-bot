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
    # စာပါပါ၊ ပုံနဲ့တွဲပါပါ ဖတ်ရှုနိုင်ရန်
    text = update.message.text or update.message.caption
    if not text:
        return

    # စာထဲမှ နံပါတ်များကို သီးသန့် ရှာဖွေခြင်း
    numbers = re.findall(r'\d+', text)
    
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

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Group ထဲက စာအားလုံးနှင့် Photo Caption များကို ဖတ်ရန်
    app.add_handler(MessageHandler((filters.TEXT | filters.CAPTION) & ~filters.COMMAND, handle_message))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
