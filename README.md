# LDAPMigrate

## What is LDAPMigrate?

The purpose of this script is to transfer entries from one LDAP environment to another.
For instance if you have: dev, qa, stage and prod LDAP environments that are separate from one another.
You may not always want to copy the whole database over when there is a couple of entries that are needed on a different environtment.
This script will allow you to specify the entry you want to copy over as well as the source and destination LDAP servers you would like to use without having to create/editing a .ldif file everytime.

## Setting this up to test.

Clone the repo.

    $ git clone https://github.com/hzgraham/ldapmigrate.git

Go into the repo's dir and setup your env variables to test.

    $ cd ldapmigrate
    $ . env/setup.py

From here you can run the command.

    $ ./bin/ldapmigrate -h

## How to authenticate?

This script will prompt for a password by default and --password is a required option but can be empty.
You can do one of things (steps 1,2 use simple auth TLS binds; step 3 is GSSAPI bind):

1. Put the password on the command line after the --password argument.
2. Don't put anything after --password in which case you will be prompted for a password. This keeps your history free of a password.
3. Don't put anything after --password and just hit return when prompted. The script will then use GSSAPI authentication.

## Example Commands

After setting up the script to test you can try the following commands.
If you just want to lookup a user and see if they exist in the destination env you can run:

    $ ./ldapmigrate uid=username lookup -m ldapserver.example.com -b dc=example,dc=com --password

To migrate from on env to another use

    $ ./ldapmigrate uid=username refresh -m ldap.source.example.com -l ldap.dest.example.com -b dc=example,dc=com --password

## RFEs

Unable to migrate a container with multiple entries.
Would like automatic group membership modifications.



