#!/usr/bin/env python

import argparse
import os

import pricedb

DB_FILE = os.path.join(os.path.expanduser("~"), ".bilag.db")
#DB_FILE = "test.db"

if not os.path.exists(DB_FILE):
    host_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(host_dir, "init.sql")
    pricedb.load_sql_file(sql_file, DB_FILE)

def add():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="PDF-scan of appedix to add")
    parser.add_argument("description", help="Description of liability/asset")
    parser.add_argument("--prefix", "-p", help="Prefix for numbering")
    args = parser.parse_args()

    if not args.file or not args.description:
        parser.print_help()
        return

    prefix = ""
    if args.prefix:
        prefix = args.prefix

    appendix_type = pricedb.getAppendixClassByPrefix(DB_FILE, prefix)
    if not appendix_type:
        print("No such appendix type. Create one with 'bilag-create'")
        return

    added = appendix_type.newAppendix(
        os.path.abspath(args.file),
        args.description
    )
    msg = f"Successfully added appendix: {args.file}\n"
    msg += f"code: {appendix_type.prefix}{added.number}"
    print(msg)


def list():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", "-p", help="Prefix for appendix type")
    args = parser.parse_args()

    if args.prefix:
        cls = pricedb.getAppendixClassByPrefix(DB_FILE, args.prefix)
        for a in cls.getAllAppendices():
            print(a)
    else:
        for cls in pricedb.getAllAppendixClasses(DB_FILE):
            for a in cls.getAllAppendices():
                print(a)


def create():
    parser = argparse.ArgumentParser(
        description="Creates appendix types and adds them to the database."
    )
    parser.add_argument("--prefix", "-p", help="Prefix for numbering")
    parser.add_argument("--startnum", "-n", help="Number to start counting from")
    parser.add_argument("description", help="Description of appendix type")

    args = parser.parse_args()

    if not args.description:
        parser.print_help()
        return

    prefix = ""
    if args.prefix:
        prefix = args.prefix

    num = 0
    if args.startnum:
        num = args.startnum

    appType = pricedb.AppendixClass(
        DB_FILE,
        args.description,
        prefix=prefix,
        counter=num,
    )
    appType.save()
    print("Saved to database.")
