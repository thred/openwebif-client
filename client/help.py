import commands
import config


def consume():
    key = config.popArg(1)

    if commands.knows(key):
        commands.help(key)
        return

    print("""\
Usage: owifc COMMAND [OPTION ...]

Known COMMANDs are:
""")

    for key in commands.keys():
        print(key + " " + "."*(16-len(key)) + " " + commands.describe(key))

    print("""
You can type "owifc help COMMAND" for more information.

Common OPTIONs are:

(--host | -h) HOST ................... The host of your OpenWebif Server.
(--bouquet | -b) BOUQUET ............. The bouquet.
--email-to address ................... Email the result to the specified address.
--smtp username:password@host:port ... The SMTP server for sending mails.
--smtps username:password@host:port .. The secure SMTP server for sending mails.
(--file | -f) FILE ................... Read the params from the file (line by line).
(--pretty | -p) ...................... Pretty print.
(--debug | -X) ....................... Enable debug output.

If the bouquet is omnitted, it uses the first (default) one.
""")


def help():
    print("""\
Usage: owifc help COMMAND

Provides detailed information about the command.""")


commands.register("help", "Provides some help.",
                  lambda: consume(), lambda: help())
