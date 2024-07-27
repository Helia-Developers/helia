import os
import sqlite3

main = os.path.join("db/botmaindata.db")


def insert_table(table_name, name1, name2):
    return f"INSERT INTO {table_name}({name1}, {name2}) VALUES(?,?)"


def update_table(table_name, name1, nm1, name2, nm2):
    return f"UPDATE {table_name} SET {name1} = {nm1} WHERE {name2} = {nm2}"


def select_table(table_name, name1, name2, nm2):
    return f"SELECT {name1} FROM {table_name} WHERE {name2} = {nm2}"


def delete_table(table_name, name1, nm1):
    return f"DELETE FROM {table_name} WHERE {name1} = {nm1}"


def control():
    base = sqlite3.connect(main)
    print("[DB] Connected to sqlite")
    cursor = base.cursor()
    tables = ["welcome", "goodbye"]
    for table in tables:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table}(guild_id TEXT, channel_id TEXT, text TEXT)"
        )
    cursor.execute("CREATE TABLE IF NOT EXISTS submit(guild_id TEXT, channel_id TEXT)")

    cursor.execute("CREATE TABLE IF NOT EXISTS prefixes(guild_id TEXT, prefix TEXT)")

    cursor.execute("CREATE TABLE IF NOT EXISTS verify(guild_id TEXT, role_id TEXT)")

    base.commit()
    cursor.close()
    base.close()
