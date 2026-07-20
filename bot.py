import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Bot Token အသစ်
TOKEN = "8899600101:AAH0_kwUb6WfPEbX1g31zakyo5v7IjBPsmM"
# သင့်ရဲ့ Admin Telegram User ID
ADMIN_ID = 8643293859

# /start နှိပ်လျှင် ပထမဆုံးပေါ်မည့် Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Telegram Account Service (SMS)", callback_data="srv_sms")],
        [InlineKeyboardButton("🔄 Telegram Old Account Recover", callback_data="srv_old")],
        [InlineKeyboardButton("🔓 Telegram Hack Account Recovery", callback_data="srv_hack")],
        [InlineKeyboardButton("📦 Telegram Readymade Account", callback_data="srv_ready")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ Telegram Service Center မှ ကြိုဆိုပါတယ်။\n\n"
        "အောက်ပါ Service များထဲမှ လိုအပ်သည်ကို ရွေးချယ်ပါ -"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup)

# ခလုတ်နှိပ်လိုက်သောအခါ လုပ်ဆောင်ချက်
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # ရွေးချယ်လိုက်သော Service ကို မှတ်သားထားမည်
    service_names = {
        "srv_sms": "Telegram Account Service (SMS fee ကျော်ပေးခြင်း)",
        "srv_old": "Telegram Old Account Recover",
        "srv_hack": "Telegram Account Hack Recovery",
        "srv_ready": "Telegram Readymade Account"
    }
    
    if data in service_names:
        context.user_data['selected_service'] = service_names[data]
        
        # Service ပေါ်မူတည်၍ တောင်းမည့် Form မေးခွန်းများ
        if data == "srv_ready":
            prompt = f"ရွေးချယ်ထားသော Service: *{service_names[data]}*\n\nအကောင့်အရေအတွက် ဘယ်လောက် လိုချင်ပါသလဲ? (ဖုန်းနံပါတ် သို့မဟုတ် အသေးစိတ် ဖြည့်ပေးပါ)"
        else:
            prompt = f"ရွေးချယ်ထားသော Service: *{service_names[data]}*\n\nကျေးဇူးပြု၍ သက်ဆိုင်ရာ Telegram ဖုန်းနံပါတ်နှင့် အသေးစိတ် အချက်အလက်များကို ဖြည့်ပေးပါ:"
            
        await query.edit_message_text(text=prompt, parse_mode="Markdown")

# ဖောက်သည်က စာသား/ဖောင် ဖြည့်သွင်းလိုက်သောအခါ
async def receive_form_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_input = update.message.text
    selected_service = context.user_data.get('selected_service')
    
    # Service မရွေးရသေးဘဲ စာပို့မိပါက ပထမဆုံး /start ပြန်ခိုင်းရန်
    if not selected_service:
        await update.message.reply_text("ကျေးဇူးပြု၍ ပထမဆုံး /start ကို နှိပ်ပြီး Service တစ်ခုကို အရင်ရွေးချယ်ပေးပါ။")
        return

    # Admin ထံသို့ ပို့မည့် Noti စာသား
    admin_message = (
        "🚨 **Order အသစ် ဝင်ရောက်လာပါပြီ!** 🚨\n\n"
        f"🛠 **Service:** {selected_service}\n"
        f"👤 **Customer:** @{user.username or 'No Username'} (ID: {user.id})\n"
        f"📝 **ဖြည့်ထားသော အချက်အလက်:**\n{user_input}"
    )
    
    # Admin ထံ Noti ပို့ရန်
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Admin ထံ Noti ပို့မရပါ: {e}")
        
    # ဖောက်သည် (Customer) ဘက်သို့ အတည်ပြုစာ ပို့ရန်
    success_text = (
        "✅ **Order တင်ခြင်း အောင်မြင်ပါသည်။**\n\n"
        "သင့်ရဲ့ အချက်အလက်များကို လက်ခံရရှိပါပြီ။ Admin မှ မကြာမီ ဆက်သွယ်ပေးပါမည်။\n\n"
        "ပင်မမီနူးသို့ ပြန်သွားရန် /start ကို နှိပ်ပါ။"
    )
    await update.message.reply_text(success_text, parse_mode="Markdown")
    
    # Data များကို ရှင်းလင်းခြင်း
    context.user_data.clear()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), receive_form_data))
    
    print("Service Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
