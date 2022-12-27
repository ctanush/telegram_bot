import logging 
import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext
import vsgoogle
import os
 #Enable logging
 
from telegram import Update,Bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',
                    level=logging.INFO)

log_msg = logging.getLogger(__name__)
                    
Tokenid = '5904974752:AAFjKeEZ2KM7x0jWVQQ5eq9_WVh_0Wsa9C4'
                    
def e_stic(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id , sticker=update.message.sticker.file_id)

def error(bot,update):
    log_msg.error("Update '%s'  caused '%s' error", update, update.error)#update.error contains error if caused due to update.

def start(update: Update,context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
##    print(update.to_dict().keys(),first_name)
    update.message.reply_text("hi {} {}".format(first_name))

def msg_handler(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)

def receive_doc(bot, update):
    message = update.message
    file_id = message.document.file_id
    chat_id = update.message.chat_id
    ocr_file(bot,update,file_id,chat_id)

def receive_image(bot,update):
    message = update.message
    file_id = message.photo[-1].file_id
    chat_id = update.message.chat_id
    ocr_file(bot,update,file_id,chat_id)
    
def ocr_file(bot,update,file_id,chat_id):
    filepath = os.path.expanduser('~') + '/' + file_id
    print(filepath)
    bot.send_message(chat_id=chat_id, text="Please hold on...")
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    file = bot.get_file(file_id).download(filepath)
    
    ocr_text = vsgoogle.read_image(filepath)
    bot.send_message(chat_id=chat_id, text='Here you go:\n\n' + str(ocr_text))
    os.remove(filepath)



def main() :
         updater = Updater(Tokenid)
                    
         dp = updater.dispatcher
         
         dp.add_handler(CommandHandler("start",start))
         dp.add_handler(CommandHandler("help",help))
         dp.add_handler(MessageHandler(Filters.text,msg_handler)) 
         dp.add_handler(MessageHandler(Filters.sticker,e_stic))
         dp.add_handler(MessageHandler(Filters.document, receive_doc))
         dp.add_handler(Filters.photo, receive_image)
         dp.add_error_handler(error)
         
         
         log_msg.info("Start Polling...")
         updater.start_polling()
         updater.idle()
         
         
if __name__ == "__main__":
             main()