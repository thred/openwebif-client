# Purpose

This client currently serves one main purpose:

It scanns the EPG provided by the [OpenWebIF](https://github.com/E2OpenPlugins/e2openplugin-OpenWebif) on the Dreambox for search terms, that are specified in a file, and mails to the result to an email address.

The client is written in Python 2, in order to be executed as a cron job on the Dreambox itself with the following command: 

```
./owifc notify -h localhost -f /home/root/ow.params --email-to me@...
```
(the SMTPs has been specified using the config, see below)

The `ow.params` contains the search terms similar to the `search.txt` sample file.

Beside of this, the project can be used as a template for other scripts based on the web interface of the Dreambox.

# Email to Gmail

In order to enable sending emails, specifiy the SMTPS parameter. Using Gmail this looks like:

```
--smtps username:password@smtp.gmail.com:465
```

You can store this in the global configuration (`~/.owifc.conf`), to avoid passing the parameter on each invocation. But be aware, that the password won't be encoded.

```
./owifc config set smtps username:password@smtp.gmail.com:465
```

Make sure to [allow less secure apps to access your account](https://support.google.com/accounts/answer/6010255). If you have 2-step verification enabled you have to [sign in using App Passwords](https://support.google.com/accounts/answer/185833).