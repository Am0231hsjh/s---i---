
import telebot
from telebot import types

# توكن البوت (حطي التوكن هنا أو خليها في ملف خارجي)
TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = telebot.TeleBot(TOKEN)

# قاعدة بيانات مؤقتة (يمكن استبدالها بقاعدة بيانات حقيقية لاحقا)
users = {}
admins = set()
muted_users = set()
banned_users = set()
allowed_channels = set()
games_active = False
music_active = False
subscribed_users = set()

channel_username = '@Stra_wbry2'  # اسم القناة العامة

# رسالة الترحيب والاشتراك
welcome_message = f"مرحبا! اشترك في القناة {channel_username} ثم اكتب /تحقق لتفعيلك."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['تحقق'])
def check_subscription(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        status = bot.get_chat_member(channel_username, user_id).status
        if status in ['member', 'administrator', 'creator']:
            subscribed_users.add(user_id)
            bot.reply_to(message, "تم التحقق من اشتراكك! يمكنك الآن التحدث في الجروب.")
        else:
            bot.reply_to(message, f"يرجى الاشتراك في القناة {channel_username} أولاً.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحقق، تأكد من الاشتراك في القناة: {str(e)}")

# مثال أوامر كتم وطرد
@bot.message_handler(commands=['كتم'])
def mute_user(message):
    if message.reply_to_message:
        user_to_mute = message.reply_to_message.from_user.id
        muted_users.add(user_to_mute)
        bot.reply_to(message, "تم كتم المستخدم.")
    else:
        bot.reply_to(message, "استخدم الأمر مع الرد على رسالة الشخص المطلوب كتمه.")

@bot.message_handler(commands=['تكلم'])
def unmute_user(message):
    if message.reply_to_message:
        user_to_unmute = message.reply_to_message.from_user.id
        muted_users.discard(user_to_unmute)
        bot.reply_to(message, "تم رفع الكتم عن المستخدم.")
    else:
        bot.reply_to(message, "استخدم الأمر مع الرد على رسالة الشخص المطلوب رفع الكتم عنه.")

# فلترة الرسائل المحظورة
@bot.message_handler(func=lambda m: True)
def filter_messages(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        return
    if user_id not in subscribed_users:
        bot.reply_to(message, welcome_message)
        return
    if user_id in muted_users:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return
    # هنا يمكن إضافة فلترة الكلمات السيئة أو الصور الإباحية
    # مثال: حذف الرسائل التي تحتوي على كلمات معينة
    forbidden_words = ['كلمة_سيئة1', 'كلمة_سيئة2']
    text = message.text.lower() if message.text else ''
    for word in forbidden_words:
        if word in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.reply_to(message, "هذه الكلمة ممنوعة هنا.")
            except:
                pass
            return
    bot.send_message(message.chat.id, f"رسالتك مسموح بيها: {message.text}")

# بدء تشغيل البوت
if __name__ == '__main__':
    print("بوت شادو الحارس شغال!")
    bot.infinity_polling()
