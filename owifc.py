#!/bin/python

import sys

import client.about
import client.bouquets
import client.commands
import client.config
import client.epg
import client.help

import codecs
import locale

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

key = client.config.command

if not client.commands.knows(key):
    print("Unknown COMMAND: " + key)
    print("For help run: owifc help")
else:
    client.commands.consume(key)
