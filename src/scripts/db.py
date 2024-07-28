"""
This module provides functions for interacting with a SQLite database used by the bot.

The `main` variable holds the path to the SQLite database file.

The `insert_table`, `update_table`, `select_table`, and `delete_table` functions generate SQL queries for performing common database operations on tables.

The `control` function sets up the database, creating the necessary tables if they don't already exist.
"""

import os
import sqlite3

cwd = os.getcwd()
parent_dir = os.path.abspath(cwd + "/../")

main = os.path.join(parent_dir + "\db\botmaindata.db")


def insert_table(table_name, name1, name2):
    return f"INSERT INTO {table_name}({name1}, {name2}) VALUES(?,?)"


def update_table(table_name, name1, nm1, name2, nm2):
    return f"UPDATE {table_name} SET {name1} = {nm1} WHERE {name2} = {nm2}"


def select_table(table_name, name1, name2, nm2):
    return f"SELECT {name1} FROM {table_name} WHERE {name2} = {nm2}"


def delete_table(table_name, name1, nm1):
    return f"DELETE FROM {table_name} WHERE {name1} = {nm1}"


def control():
    print(cwd)
    print(parent_dir)
    print(main)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(main), exist_ok=True)

    try:
        base = sqlite3.connect(main)
        print("[DB] Connected to sqlite")
        cursor = base.cursor()
        tables = ["welcome", "goodbye"]
        for table in tables:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table}(guild_id TEXT, channel_id TEXT, text TEXT)"
            )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS submit(guild_id TEXT, channel_id TEXT)"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS prefixes(guild_id TEXT, prefix TEXT)"
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS verify(guild_id TEXT, role_id TEXT)")

        base.commit()
    except sqlite3.OperationalError as e:
        
        print(f"[DB] Error: {e}")
        print(f"[DB] Unable to open database file: {main}")
        print("[DB] Please check file permissions and path.")
        raise sqlite3.OperationalError
    finally:
        if "cursor" in locals():
            cursor.close()
        if "base" in locals():
            base.close()
