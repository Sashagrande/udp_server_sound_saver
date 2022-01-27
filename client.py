import asyncio
import socket
import wave
import websockets
HOST, PORT = 'localhost', 14000


async def send_file(input_file: str) -> str:
    uri = 'ws://localhost:14000'
    async with websockets.connect(uri) as websocket:
        wf = wave.open(input_file, "rb")
        await websocket.send('{ "config" : { "filename" : "%s" } }' % input_file)
        buffer_size = int(wf.getframerate() * 0.2)  # 0.2 seconds of audio
        while True:
            data = wf.readframes(buffer_size)
            if len(data) == 0:
                break
            await websocket.send(data)
        await websocket.send('finish')
        result = await websocket.recv()
        return True if 'approved' in result else False


def main(file):
    result = asyncio.run(send_file(file))
    print(result)


if __name__ == '__main__':
    main('test.wav')
