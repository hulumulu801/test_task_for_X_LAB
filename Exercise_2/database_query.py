#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import psycopg2
##################################################################################################################
def get_query_data(date):
    con = None
    dict = {}
    count_ao = 0
    count_human = 0
    initial_time_duration_audio_human = 0.0
    initial_time_duration_audio_ao = 0.0
    the_person_answered_positively = 0
    the_person_answered_negatively = 0
    try:
        con = psycopg2.connect(
                                database = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                user = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                password = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-",
                                host = "127.0.0.1",
                                port = "5432"
                                )
        cur = con.cursor()
        cur.execute("SELECT * FROM ИМЯ_БАЗЫ_ДАННЫХ WHERE date = %s", (str(date), ))
        row = cur.fetchone()
        while row is not None:
            all_date_day = row[0]
            duration_audio = row[5]
            ao_or_human = row[3]
            if "АО" == str(ao_or_human):
                count_ao += 1
                dict["Дата"] = str(date)
                initial_time_duration_audio_ao += float(duration_audio)
            elif "Человек" == str(ao_or_human):
                count_human += 1
                dict["Дата"] = str(date)
                initial_time_duration_audio_human += float(duration_audio)
            elif "1" == str(ao_or_human):
                the_person_answered_positively += 1
            elif "0" == str(ao_or_human):
                the_person_answered_negatively += 1
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    dict["Количество людей за указанную дату"] = str(count_human)
    dict["Количество АО за указанную дату"] = str(count_ao)
    dict["Общая продолжительность аудио записей с участием людей"] = str(initial_time_duration_audio_human)
    dict["Общая продолжительность аудио записей с участием АО"] = str(initial_time_duration_audio_ao)
    dict["Общее количество положительных ответов"] = str(the_person_answered_positively)
    dict["Общее количество отрицательных ответов"] = str(the_person_answered_negatively)
    return dict
##################################################################################################################
def save_sql_query(dict_data):
    try:
        name_file = "sql_query.csv"
        path = os.path.abspath("./")
        abs_path = path + "/" + name_file
        if not os.path.exists(abs_path):
            with open(abs_path, "a") as f:
                writer = csv.DictWriter(f, fieldnames = ["Дата",
                                                         "Количество людей за указанную дату",
                                                         "Количество АО за указанную дату",
                                                         "Общая продолжительность аудио записей с участием людей",
                                                         "Общая продолжительность аудио записей с участием АО",
                                                         "Общее количество положительных ответов",
                                                         "Общее количество отрицательных ответов"], delimiter = ";")
                writer.writeheader()
        with open(abs_path, "a") as f:
            writer = csv.writer(f)
            writer.writerow((
                                dict_data["Дата"],
                                dict_data["Количество людей за указанную дату"],
                                dict_data["Количество АО за указанную дату"],
                                dict_data["Общая продолжительность аудио записей с участием людей"],
                                dict_data["Общая продолжительность аудио записей с участием АО"],
                                dict_data["Общее количество положительных ответов"],
                                dict_data["Общее количество отрицательных ответов"]
            ))
    except KeyError as e:
        if "'Дата'" == str(e):
            print("За указанную дату ни чего не найдено!")
##################################################################################################################
def main():
    date = input("Введите дату в формате: год-месяц-число \nНапример: 2020-12-05 \n")
    dict_data = get_query_data(date)
    save_sql_query(dict_data)
##################################################################################################################
if __name__ == "__main__":
    main()
