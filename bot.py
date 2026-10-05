import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

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

import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8917617373:AAGJSuFAtfAROKjTs2JDfkBr-CTSgSuKCC8"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    numbers = re.findall(r'\d+', text)
    
    if numbers:
        # HTML Format ပြောင်းထားသဖြင့် Parse Error လုံးဝ မတက်တော့ပါ
        formatted_numbers = [f"<code>{num}</code>" for num in numbers]
        reply_text = "👇 နှိပ်လိုက်ပါက တန်းပြီး Copy ကူးသွားပါမည် -\n\n" + "\n".join(formatted_numbers)
        
        await update.message.reply_text(
            text=reply_text,
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text("စာထဲတွင် Number တစ်ခုမျှ မတွေ့ပါ။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("MacBook တွင် Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
