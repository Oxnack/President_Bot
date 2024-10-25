import telebot
import csv
from telebot import types



# Замените на ваш токен и ID администратора
TOKEN = '8075240704:AAGxHg_ZRz863pU0oao5VEc2zyxFdIZpE0c'
ADMIN_CHAT_ID = '5176418706'

bot = telebot.TeleBot(TOKEN)

# Хранение заявок
user_requests = {}

data = [
    ["user_id", "username"]
]



@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id    
    username = message.from_user.usernam
    save_user(user_id, username) 

    bot.send_message(message.chat.id, "Добро пожаловать! Отправьте свою заявку.")


@bot.message_handler(func=lambda message: True)
def handle_request(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_requests[user_id] = message.text 
    print(message.text)

    save_user(user_id, username)

    # Создаем кнопки для администратора
    markup = types.InlineKeyboardMarkup()
    accept_button = types.InlineKeyboardButton("Принять", callback_data=f'accept_' + str(user_id) + "_" + username)
    reject_button = types.InlineKeyboardButton("Отклонить", callback_data=f'reject_' + str(user_id) + "_" + username)
    
    markup.add(accept_button, reject_button)

    # Отправляем заявку админу
    bot.send_message(ADMIN_CHAT_ID, f"Новая заявка: "  + message.text +  "\n user ID: " + str(user_id) + "\n user nickname: @" + username, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = int(call.data.split('_')[1])
    username = str(call.data.split("_")[2])

    print(call.data)
    
    if call.data.startswith('accept'):
        bot.send_message(call.message.chat.id, "Заявка принята. Напишите ответ пользователю. \n userID: " + str(user_id) + "\n username: @" + username)
        bot.register_next_step_handler(call.message, lambda msg: send_response(msg, user_id))
        
    elif call.data.startswith('reject'):
        bot.send_message(user_id, "Ваша заявка отклонена.")
        bot.answer_callback_query(call.id, "Заявка отклонена.")

def send_response(message, user_id):
    response_text = message.text
    bot.send_message(user_id, f"Ответ от администратора: {response_text}")


def save_user(user_id, username):
    ok = True
    for elm in data:
        if elm[1] == username:
            ok = False

    if ok == True:
        data.append([user_id,username])


        with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)                               
            writer.writerows(data)
        print("данные записаны")

def data_reader():
    # Чтение данных из CSV-файла                           
    with open('data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)                            
        data = []                                         
        for row in reader:                                
            data.append(row)



data_reader()
print("данные прочитаны") 

if __name__ == '__main__':
    bot.polling(none_stop=True)


#####




