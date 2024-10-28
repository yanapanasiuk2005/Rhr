import wave
import numpy as np

def hide_data(sound_path, file_to_hide, output_path):
    # Відкриття звукового файлу
    song = wave.open(sound_path, mode='rb')
    # Читання кадрів з аудіофайлу
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Відкриття файлу з даними для приховування
    with open(file_to_hide, 'r') as f:
        data = f.read()

    # Додавання маркера кінця повідомлення
    data += '###'
    # Перетворення даних у бінарний формат
    data = ''.join([format(ord(i), '08b') for i in data])
    
    # Перевірка на переповнення
    if len(data) > len(frame_bytes):
        raise ValueError("Error: Insufficient bytes, need larger file size.")

    # Вбудовування даних у аудіофайл
    for i in range(len(data)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(data[i])

    # Перетворення назад у байти
    frame_modified = bytes(frame_bytes)

    # Запис у новий файл
    with wave.open(output_path, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    song.close()

# Функція для видобування інформації з аудіофайлу
def extract_data(sound_path):
    song = wave.open(sound_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Видобування даних з аудіофайлу
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Перетворення бітів у символи
    string = "".join(chr(int("".join(map(str, extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))
    
    # Вирізання за маркером кінця повідомлення
    decoded = string.split("###")[0]

    song.close()
    return decoded
# Приклад використання
if __name__ == "__main__":
    # Приховування даних
    hide_data("C:\testPythone\file_example_WAV_1MG.wav", "C:\testPythone\test.txt", "C:\testPythone\16-bit-8kHz-noBext-mono.wav")

    # Видобування даних
    extracted_data = extract_data("C:\testPythone\16-bit-8kHz-noBext-mono.wav")
    print("Extracted Data:", extracted_data)
 
