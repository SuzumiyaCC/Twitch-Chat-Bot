import os
import time
import random
import asyncio
import socks
import socket
from pystyle import Center, Colors, Colorate

# Настройки прокси
proxy_servers = [
    {"host": "109.172.86.33", "port": 54333},
    {"host": "116.202.48.78", "port": 52497},
    {"host": "65.21.164.240", "port": 39846},    

]

# Настройки Twitch IRC
server = "irc.chat.twitch.tv"
port = 6667

# Чтение токенов и сообщений
with open("oauths.txt", "r") as file:
    oauths = [line.strip() for line in file.readlines()]

with open("messages.txt", "r", encoding='utf-8') as file:
    messages = [line.strip() for line in file.readlines()]

# Асинхронная функция для отправки сообщения
async def send_message(oauth, channel, message, proxy):
    try:
        # Настройка прокси
        socks.set_default_proxy(socks.SOCKS5, proxy["host"], proxy["port"])
        socket.socket = socks.socksocket

        # Подключение к Twitch IRC
        reader, writer = await asyncio.open_connection(server, port)

        # Авторизация и отправка сообщения
        writer.write(f"PASS {oauth}\n".encode())
        writer.write(f"NICK bot\n".encode())
        writer.write(f"JOIN #{channel}\n".encode())
        await writer.drain()

        writer.write(f"PRIVMSG #{channel} :{message}\n".encode())
        await writer.drain()

        print(f"[{time.strftime('%X')}] Sent message from token: {oauth} - Proxy: {proxy['host']}:{proxy['port']} - {message}")

        # Закрытие соединения
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Error sending message: {e}")

# Основная асинхронная функция
async def main():
    channel = input(Colorate.Vertical(Colors.green_to_blue, "КАНАЛ ДАЙ ДАЙ ТВАРЬ: "))
    message_option = input(Colorate.Vertical(Colors.green_to_blue, "ЧЕ ДЕЛАЕМ? (1. ОТПРАВЛЯЕМ С ОДНОГО, 2. ОТПРАВЛЯЕМ С РАНДОМНЫХ ТОКЕНОВ): "))

    while True:  # Бесконечный цикл
        tasks = []
        if message_option == "1":
            # Отправка с одного токена
            oauth = oauths[0]
            for _ in range(10):  # Отправка 10 сообщений
                proxy = random.choice(proxy_servers)
                message = random.choice(messages)
                task = asyncio.create_task(send_message(oauth, channel, message, proxy))
                tasks.append(task)
        else:
            # Отправка с рандомных токенов
            for oauth in oauths:
                proxy = random.choice(proxy_servers)
                message = random.choice(messages)
                task = asyncio.create_task(send_message(oauth, channel, message, proxy))
                tasks.append(task)

        # Ожидание завершения всех задач
        await asyncio.gather(*tasks)

        # Случайный промежуток времени перед следующим запуском
        sleep_time = random.uniform(15, 20)  # От 1 до 3 минут
        print(f"[{time.strftime('%X')}] Waiting for {sleep_time:.2f} seconds before the next cycle...")
        await asyncio.sleep(sleep_time)

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())