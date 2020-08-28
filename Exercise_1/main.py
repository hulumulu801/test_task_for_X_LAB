#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wave
import psycopg2
import contextlib
from uuid import uuid4
from datetime import datetime
from tinkoff_voicekit_client import ClientSTT
################################################################################################################
def get_audio_file(path_audio_file):
    try:
        path = os.path.abspath(path_audio_file)
        return path
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def get_duration_wav(path_audio_file):
    try:
        with contextlib.closing(wave.open(str(path_audio_file), "r")) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def get_recognition_audio_file_s1(API_KEY, SECRET_KEY, audio_file):
    try:
        client = ClientSTT(API_KEY, SECRET_KEY)
        audio_config = {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 8000,
            "num_channels": 1
        }
        response = client.recognize(str(audio_file), audio_config)
        for r in response:
            lists = r["alternatives"]
            for list in lists:
                recognition_text = list["transcript"]
                if "автоответчик" in str(recognition_text) or "после сигнала" in str(recognition_text):
                    return "АО", str(recognition_text)
                elif "алло" in str(recognition_text) or "слушаю" in str(recognition_text) or "удобно" in str(recognition_text) or "нет" in str(recognition_text) or "я" in str(recognition_text):
                    return "Человек", str(recognition_text)
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def get_recognition_audio_file_s2(API_KEY, SECRET_KEY, audio_file):
    try:
        client = ClientSTT(API_KEY, SECRET_KEY)
        audio_config = {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 8000,
            "num_channels": 1
        }
        response = client.recognize(str(audio_file), audio_config)
        for r in response:
            lists = r["alternatives"]
            for list in lists:
                recognition_text = list["transcript"]
                if "нет" in str(recognition_text) or "не удобно" in str(recognition_text) or "неудобно" in str(recognition_text) or "до свидания" in str(recognition_text):
                    return str(0), str(recognition_text)
                elif "да удобно" in str(recognition_text) or "говорите" in str(recognition_text):
                    return str(1), str(recognition_text)
                else:
                    return "Ни чего не найденно", str(recognition_text)
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def save_log_file(date, time, id, result_of_action, number_phone, duration_wav, recognition_result):
    try:
        data = {
        "Дата": str(date),
        "Время": str(time),
        "Уникальный id": str(id),
        "Результат действия": str(result_of_action),
        "Номер телефона": str(number_phone),
        "Продолжительность аудио": str(duration_wav),
        "Результат распознавания": str(recognition_result)
        }
        name_file = "log_file.csv"
        path = os.path.abspath("./")
        abs_path = path + "/" + name_file
        if not os.path.exists(abs_path):
            with open(abs_path, "a") as f:
                writer = csv.DictWriter(f, fieldnames = ["Дата", "Время", "Уникальный id", "Результат действия", "Номер телефона", "Продолжительность аудио", "Результат распознавания"], delimiter = ';')
                writer.writeheader()
        with open(abs_path, "a") as f:
            writer = csv.writer(f)
            writer.writerow((
                                data["Дата"],
                                data["Время"],
                                data["Уникальный id"],
                                data["Результат действия"],
                                data["Номер телефона"],
                                data["Продолжительность аудио"],
                                data["Результат распознавания"]
            ))
        return str(abs_path)
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def save_new_file(data_csv):
    try:
        file = str(data_csv).split("log_file.csv")[0] + "new_file.txt"
        with open(str(data_csv), "r") as f:
            reader = csv.reader(f)
            for row in reader:
                pass
                counter = 0
            for r in row:
                with open(str(file), "a") as f:
                    counter += 1
                    if counter <= 6:
                        f.write(str(r) + ",")
                    elif counter >= 7:
                        f.write(str(r))
        return file
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def save_data_base(new_file_csv):
    try:
# Подключение к базе
        con = psycopg2.connect(
                                database = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                user = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                password = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                host = "127.0.0.1",
                                port = "5432"
                                )
        cur = con.cursor()
# Создание базы данных
        # cur.execute('''CREATE TABLE ТУТ_ИМЯ_БАЗЫ_ДАННЫХ
        #       (DATE TEXT NOT NULL,
        #       TIME TEXT NOT NULL,
        #       ID TEXT NOT NULL,
        #       RESULT_OF_ACTION TEXT NOT NULL,
        #       NUMBER_PHONE TEXT NOT NULL,
        #       DURATION_WAV TEXT NOT NULL,
        #       RECOGNITION_RESULT TEXT NOT NULL);''')
# Чтение из csv файла
        with open(str(new_file_csv), "r") as f:
            cur.copy_from(f, "ТУТ_ИМЯ_БАЗЫ_ДАННЫХ", sep = ",")
        con.commit()
        cur.close()
        con.close()
        os.remove(new_file_csv)
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
def main():
    try:
        API_KEY = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
        SECRET_KEY = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
        path_audio_file = sys.argv[1]
        number_phone = sys.argv[2]
        write_datebase = sys.argv[3]
        stage_recognition_audio_file = sys.argv[4]

        audio_file = get_audio_file(path_audio_file)

        date_and_time = datetime.now()
        date = str(date_and_time).split(" ")[0]
        time = str(date_and_time).split(" ")[-1]
        id = str(uuid4())
        duration_wav = get_duration_wav(audio_file)

        if "stage-1" in stage_recognition_audio_file.lower():
            # Этап распознования - 1
            result_of_action_s1, recognition_result_s1 = get_recognition_audio_file_s1(API_KEY, SECRET_KEY, audio_file)
            data_csv = save_log_file(date, time, id, result_of_action_s1, number_phone, duration_wav, recognition_result_s1)
        elif "stage-2" in stage_recognition_audio_file.lower():
            # Этап распознования - 2
            result_of_action_s2, recognition_result_s2 = get_recognition_audio_file_s2(API_KEY, SECRET_KEY, audio_file)
            data_csv = save_log_file(date, time, id, result_of_action_s2, number_phone, duration_wav, recognition_result_s2)
        if "1" in write_datebase:
            print("Записываю в базу данных")
            new_file_csv = save_new_file(data_csv)
            save_data_base(new_file_csv)
        os.remove(str(audio_file))
    except Exception as e:
        path = "./"
        abs_path = os.path.abspath(path)
        log_fail = abs_path + "/" + "log_fail.txt"
        with open(str(log_fail), "a+") as file_log_fail:
            file_log_fail.write(str(e) + "\n")
################################################################################################################
if __name__ == "__main__":
    main()
