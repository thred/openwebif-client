# Purpose

This client currently serves one main purpose:

It scanns the EPG for search terms, that are specified in a file, and mails to the result to an email address.

# Email

In order to enable sending emails, specifiy the SMTPS parameter. Using Gmail this looks like:

```
-smtps username:password@smtp.gmail.com:465
```

Make sure to [allow less secure apps to access your account](https://support.google.com/accounts/answer/6010255). If you have 2-step verification enabled you have to [sign in using App Passwords](https://support.google.com/accounts/answer/185833).