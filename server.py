import json
import os
import asyncio
import websockets
import concurrent.futures
import logging


def read_socket(filename, data):
    global path
    with open(f'{path}/{filename}', 'wb') as file:
        file.write(data)


async def save_sound(websocket):
    global pool, loop
    message = await websocket.recv()
    filename = 'undefinedSound'
    if isinstance(message, str) and 'config' in message:
        filename = json.loads(message)['config']['filename']
        logging.info(f'Принимаю файл {filename}')
    file = bytes()
    while True:
        chunk = await websocket.recv()
        if isinstance(chunk, str) and 'finish' in chunk:
            logging.info(f'Сохранил файл {filename}')
            break
        file += chunk
    await websocket.send('approved')
    await loop.run_in_executor(pool, read_socket, filename, file)


def start():
    global path
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(path):
        os.mkdir(path)
    address, port = 'localhost', 14000
    start_server = websockets.serve(
        save_sound, address, port)
    logging.info("Listening on %s:%d", address, port)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    path = 'received_files'
    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))
    loop = asyncio.get_event_loop()
    start()
