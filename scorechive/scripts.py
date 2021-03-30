import click
import columnize
import sqlite3
import sys
import warnings

from itertools import chain
from pathlib import Path


def create_db(database_name):
    pass

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE "Score" (
	                   "ID" INTEGER,
                       "Title" TEXT NOT NULL,
                       "YearPublished" INTEGER NOT NULL,
                   PRIMARY KEY("ID"));""")

    cur.execute("""CREATE TABLE "Composer" (
                       "ID"INTEGER,
                       "ScoreID" INTEGER NOT NULL,
                       "FirstName" TEXT NOT NULL,
                       "MiddleName" TEXT,
                       "LastName"	TEXT,
                   PRIMARY KEY("ID"),
                   FOREIGN KEY("ScoreID") REFERENCES "Score"("ID") ON DELETE CASCADE);""")

    cur.execute("""CREATE TABLE "Arranger" (
                       "ID" INTEGER,
                       "ScoreID" INTEGER NOT NULL,
                       "FirstName" TEXT NOT NULL,
                       "MiddleName" TEXT,
                       "LastName" TEXT,
                   PRIMARY KEY("ID"),
                   FOREIGN KEY("ScoreID") REFERENCES "Score"("ID") ON DELETE CASCADE);""")

    cur.execute("""CREATE TABLE "Part" (
                       "ID" INTEGER,
                       "ScoreID" INTEGER NOT NULL,
                       "Part" TEXT NOT NULL,
                   PRIMARY KEY("ID"),
                   FOREIGN KEY("ScoreID") REFERENCES "Score"("ID") ON DELETE CASCADE);""")

    cur.execute("""CREATE TABLE "Instrument" (
                       "ID" INTEGER,
                       "ScoreID" INTEGER NOT NULL,
                       "PartID" INTEGER NOT NULL,
                       "Instrument" TEXT NOT NULL,
                   PRIMARY KEY("ID"),
                   FOREIGN KEY("ScoreID") REFERENCES "Score"("ID") ON DELETE CASCADE,
                   FOREIGN KEY("PartID") REFERENCES "Part"("ID") ON DELETE CASCADE);""")

    conn.commit()

    print(f"{database_name} has been created.")


def view_score(database_name, part, instrumentation, dates):

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    if part:
        score_id = int(input("Enter the ID of the score:\n"))

        cur.execute("""SELECT Score.ID,
                              Title,
                              YearPublished,
                              Composer.FirstName,
                              Composer.MiddleName,
                              Composer.LastName,
                              Arranger.FirstName,
                              Arranger.MiddleName,
                              Arranger.LastName,
                              Part.Part
                       FROM Score
                       LEFT JOIN Composer ON Score.ID = Composer.ScoreID
                       LEFT JOIN Arranger ON Score.ID = Arranger.ScoreID
                       LEFT JOIN Part ON Score.ID = Part.ScoreID
                       WHERE Score.ID = ?
                       ORDER BY Part.ID ASC""",(score_id,))
    elif instrumentation:
        score_id = int(input("Enter the ID of the score you would like to view:\n"))

        cur.execute("""SELECT Score.ID,
                              Title,
                              YearPublished,
                              Composer.FirstName,
                              Composer.MiddleName,
                              Composer.LastName,
                              Arranger.FirstName,
                              Arranger.MiddleName,
                              Arranger.LastName,
                              Part.Part,
                              Instrument.Instrument
                       FROM Score
                       LEFT JOIN Composer ON Score.ID = Composer.ScoreID
                       LEFT JOIN Arranger ON Score.ID = Arranger.ScoreID
                       LEFT JOIN Part ON Score.ID = Part.ScoreID
                       LEFT JOIN Instrument ON Part.ID = Instrument.PartID
                       WHERE Score.ID = ?
                       ORDER BY Instrument.ID ASC""",(score_id,))
    elif dates:
        score_id = int(input("Enter the ID of the score you would like to view:\n"))

        cur.execute("""SELECT Score.ID,
                              Title,
                              YearPublished,
                              Composer.FirstName,
                              Composer.MiddleName,
                              Composer.LastName,
                              Arranger.FirstName,
                              Arranger.MiddleName,
                              Arranger.LastName,
                              DatePerformed.DatePerformed
                       FROM Score
                       LEFT JOIN Composer ON Score.ID = Composer.ScoreID
                       LEFT JOIN Arranger ON Score.ID = Arranger.ScoreID
                       LEFT JOIN DatePerformed ON Score.ID = DatePerformed.ScoreID
                       WHERE Score.ID = ?
                       ORDER BY
                    DatePerformed.DatePerformed DESC;""",(score_id,))
    else:
        cur.execute("""SELECT Score.ID,
                              Title,
                              YearPublished,
                              Composer.FirstName,
                              Composer.MiddleName,
                              Composer.LastName,
                              Arranger.FirstName,
                              Arranger.MiddleName,
                              Arranger.LastName
                       FROM Score
                       LEFT JOIN Composer ON Score.ID = Composer.ScoreID
                       LEFT JOIN Arranger ON Score.ID = Arranger.ScoreID;""")

    # Print each entry selected in cursor
    for row in cur.fetchall():
        print(row)

    conn.commit()


def insert_parts(database_name, score_id=None, conn=None, cur=None):
    if not score_id:
        score_id = int(input("Enter the ID of the score:\n"))

        conn = sqlite3.connect(database_name)
        cur = conn.cursor()

    display_instrumentation()

    part_list = parse_instrumentation(
        input(
            """Enter a series of instruments by index or name in the desired score order, delimited by a ",".\nIf part has contains multiple instruments, add a "#" to the beginning of the part name (e.g. "#Flute").\nEnter "!Strings" for string ensemble, or !SATB for standard choir:\n"""
        )
    )

    for each in part_list:
        if each[0] == "#":

            print(f"""Entering instrumentation for part "{each[1:]}":""")

            display_instrumentation()

            instrumentation_list = parse_instrumentation(
                input(
                    """Enter a series of instruments by index or name in the desired score order, delimited by a ",".\n"""
                )
            )

            cur.execute("""INSERT INTO "main"."Part"
                                       ("ScoreID", "Part")
                           VALUES (?,?);""",(score_id, each[1:]))

            part_id = cur.execute("""SELECT MAX(ID) FROM Part;""").fetchone()[0]

            for each_instrument in instrumentation_list:
                cur.execute(
                    """
                INSERT INTO "main"."Instrument"
                            ("ScoreID", "PartID", "Instrument")
                VALUES (?,?,?);""",(score_id, part_id, each_instrument))
        else:
            cur.execute("""INSERT INTO "main"."Part"
                                       ("ScoreID", "Part")
                           VALUES (?,?);""",(score_id,each))

            part_id = cur.execute("""SELECT MAX(ID) FROM Part;""").fetchone()[0]

            cur.execute("""INSERT INTO "main"."Instrument"
                                       ("ScoreID", "PartID", "Instrument")
                           VALUES (?,?,?);""",(score_id, part_id, each))

    conn.commit()


def add_score(database_name):
    title = input("Enter the title of the score:\n")

    year_published = int(input("Enter the year the score was published:\n"))

    composers = parse_names("composer")
    arrangers = parse_names("arranger")

    if not composers and not arrangers:
        raise ValueError("You must enter at least one composer or arranger!")

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("""INSERT INTO "main"."Score"
                               ("Title", "YearPublished")
                   VALUES (?,?);""",(title, year_published))

    score_id = cur.execute("""SELECT MAX(ID) FROM Score;""").fetchone()[0]

    try:
        for each in composers:
            cur.execute("""INSERT INTO "main"."Composer"
                                       ("ScoreID", "FirstName","MiddleName","LastName")
                           VALUES (?,?,?,?);""",(score_id, each[0], each[1], each[2]))
    except (TypeError):
        pass
    try:
        for each in arrangers:
            cur.execute("""INSERT INTO "main"."Arranger"
                                       ("ScoreID", "FirstName","MiddleName","LastName")
                           VALUES (?,?,?,?);""",(score_id, each[0], each[1], each[2]))
    except (TypeError):
        pass

    insert_parts(database_name,score_id,conn,cur)


def delete_score(database_name):

    score_id = int(input("Enter the ID of the score:\n"))

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("""DELETE FROM Score
                   WHERE "ID" = ?;""",(score_id,))

    conn.commit()

    print(f"{database_name} has been deleted.")


def parse_names(role):
    names = []

    first_name = input(f"Enter the first name of the {role}:\n")
    if not first_name:
        return None
    middle_name = input(f"Enter the middle name of the {role}:\n")
    if not middle_name:
        middle_name = None
    last_name = input(f"Enter the last name of the {role}:\n")
    if not last_name:
        last_name = None
    names.append(tuple([first_name, middle_name, last_name]))
    print(
        f"Enter additional {role}s. Enter nothing if there are no additional {role}s."
    )

    while True:
        first_name = input(f"Enter the first name of the {role}:\n")
        if not first_name:
            break
        middle_name = input(f"Enter the middle name of the {role}:\n")
        if not middle_name:
            middle_name = None
        last_name = input(f"Enter the last name of the {role}:\n")
        if not last_name:
            last_name = None
        names.append(tuple([first_name, middle_name, last_name]))

    return names


def parse_instrumentation(instrumentation_input):
    with open("instrumentation_list.txt") as f:
        data = f.readlines()
        instrumentation = []
        for each in instrumentation_input.split(","):
            try:
                # Tries to append instruments by index
                instrumentation.append(data[int(each)].strip())
            except:
                # Append instruments by index with "#" modifier
                if each[0] == "#":
                    try:
                        instrumentation.append(f"#{data[int(each[1:])].strip()}")
                    except:
                        instrumentation.append(each)
                # Parses common instrument ensembles
                elif each[0] == "!":
                    if each[1:] == "Strings":
                        instrumentation.extend(
                            ["Violin", "Violin", "Viola", "Violoncello", "Double Bass"]
                        )
                    elif each[1:] == "SATB":
                        instrumentation.extend(["Soprano", "Alto", "Tenor", "Bass"])
                # Append instruments directly
                else:
                    instrumentation.append(each)
        return instrumentation


def display_instrumentation():
    with open("instrumentation_list.txt") as f:
        instrument = f.readlines()
        list = []
        for i, each in enumerate(instrument):
            list.append(f"{i}. {each.strip()}")
        print(columnize.columnize(list))
