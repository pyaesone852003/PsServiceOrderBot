import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8899600101:AAH0_kwUb6WfPEbX1g31zakyo5v7IjBPsmM"
ADMIN_ID = 8643293859

PAYMENT_INFO = (
    "\n\n--------------------------------\n"
    "ငွေပေးချေရန် နည်းလမ်းများ:\n"
    "• KPay / Wave Pay / Aya Pay / UAB Pay\n"
    "• Phone: 09779412905\n"
    "• Name: Mg Pyae Sone Aung\n"
    "--------------------------------\n"
    "ငွေလွှဲပြီးပါက ငွေလွှဲစလစ် (Screenshot) နှင့်တကွ ဆက်လက်ပေးပို့ပေးပါခင်ဗျာ။"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    
    keyboard = [
        [InlineKeyboardButton("Telegram Account Service (SMS) - 10k", callback_data="srv_sms")],
        [InlineKeyboardButton("Telegram Old Account Recover - 15k", callback_data="srv_old")],
        [InlineKeyboardButton("Telegram Hack Account Recovery - 30k", callback_data="srv_hack")],
        [InlineKeyboardButton("Telegram Readymade Account - 5k", callback_data="srv_ready")],
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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    service_names = {
        "srv_sms": "Tg new acc create (10k - ၁ သောင်းကျပ်)",
        "srv_old": "Tg old acc rc (15k - ၁ သောင်းခွဲကျပ်)",
        "srv_hack": "Tg acc hack rc (30k - ၃ သောင်းကျပ်)",
        "srv_ready": "Tg ready made acc (5k - ၅ ထောင်ကျပ်)"
    }
    
    if data in service_names:
        context.user_data['selected_service'] = service_names[data]
        
        if data == "srv_sms":
            prompt = (
                f"ရွေးချယ်ထားသော Service: {service_names[data]}\n\n"
                "ကျေးဇူးပြု၍ Telegram ဖွင့်ချင်တဲ့ ဖုန်းနံပါတ် ကို ပို့ပေးပါ။"
                + PAYMENT_INFO
            )
        elif data == "srv_old":
            prompt = (
                f"ရွေးချယ်ထားသော Service: {service_names[data]}\n\n"
                "ကျေးဇူးပြု၍ ပြန်ဆယ်ချင်တဲ့ telegram ဖွင့်ထားတဲ့ ဖုန်းနံပါတ် ကို ပို့ပေးပါ။"
                + PAYMENT_INFO
            )
        elif data == "srv_hack":
            prompt = (
                f"ရွေးချယ်ထားသော Service: {service_names[data]}\n\n"
                "ကျေးဇူးပြု၍ အောက်ပါပုံစံအတိုင်း အချက်အလက်များ ပို့ပေးပါ -\n"
                "1. ပြန်ဆယ်ချင်တဲ့ telegram ဖွင့်ထားတဲ့ ဖုန်းနံပါတ်\n"
                "2. အရင်ကချိတ်ထားတဲ့ Gmail"
                + PAYMENT_INFO
            )
        elif data == "srv_ready":
            prompt = (
                f"ရွေးချယ်ထားသော Service: {service_names[data]}\n\n"
                "အကောင့်အရေအတွက် ဘယ်လောက် လိုချင်လဲ ဖြည့်ပေးပါ။"
                + PAYMENT_INFO
            )
            
        await query.edit_message_text(text=prompt)

async def receive_form_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_input = update.message.text
    selected_service = context.user_data.get('selected_service')
    
    if not selected_service:
        await update.message.reply_text("ကျေးဇူးပြု၍ ပထမဆုံး /start ကို နှိပ်ပြီး Service တစ်ခုကို အရင်ရွေးချယ်ပေးပါ။")
        return

    admin_message = (
        "Order အသစ် ဝင်ရောက်လာပါပြီ!\n\n"
        f"Service: {selected_service}\n"
        f"Customer: @{user.username or 'No Username'} (ID: {user.id})\n"
        f"ဖြည့်ထားသော အချက်အလက်:\n{user_input}"
    )
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    except Exception as e:
        print(f"Admin ထံ Noti ပို့မရပါ: {e}")
        
    success_text = (
        "Order တင်ခြင်း အောင်မြင်ပါသည်။\n\n"
        "သင့်ရဲ့ အချက်အလက်များနှင့် ငွေလွှဲအချက်အလက်များကို လက်ခံရရှိပါပြီ။ Admin မှ စစ်ဆေးပြီး ဆက်သွယ်ပေးပါမည်။\n\n"
        "ပင်မမီနူးသို့ ပြန်သွားရန် /start ကို နှိပ်ပါ။"
    )
    await update.message.reply_text(success_text)
    
    context.user_data.clear()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), receive_form_data))
    
    print("Service Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
