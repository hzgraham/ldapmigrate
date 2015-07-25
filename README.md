# LDAPMigrate

## What is LDAPMigrate?

The purpose of this script is to transfer entries from one LDAP environment to another.
For instance if you have: dev, qa, stage and prod LDAP environments that are separate from one another.
You may not always want to copy the whole database over when there is a couple of entries that are needed on a different environment.
This script will allow you to specify the entry you want to copy over as well as the source and destination LDAP servers you would like to use without having to create/edit a .ldif file everytime.

## Setting this up to test.

Clone the repo.

    $ git clone https://github.com/hzgraham/ldapmigrate.git

Go into the repo's dir and setup your env variables to test.

    $ cd ldapmigrate
    $ . env/setup

From here you can run the command.

    $ ./bin/ldapmigrate -h

## How to authenticate?

You can do one of three things (steps 1,2 use simple auth TLS binds; step 3 is GSSAPI bind):

1. If you don't use the --password option then GSSAPI will be used in which case you need a Kerberos TGT.
2. Put the password on the command line after the --password argument.
3. Don't put anything after --password in which case you will be prompted for a password. This keeps your history free of a password.

## About the ldapmigrate command and options.

The ldapmigrate script performs two functions which are identified by the "lookup" or "migrate" option seen when running.

    $ ./bin/ldapmigrate -h

Currently the syntax is to enter a user specified option identifying the LDAP entry before using either lookup or migrate.

    $ ./bin/ldapmigrate uid=username lookup -h
    $ ./bin/ldapmigrate uid=username migrate -h

Except for destination host option (--dest-host or just -d) for the "migrate" function all other options for these functions are optional.

## LDAP config sources

The LDAP config URI, BASE, and TLS_CACERT or TLS_CACERTDIR options for the "lookup" and "migrate" functions are first taken from the command line arguments.
If those options weren't used in the command then they will be taken from the ~/.ldaprc and if not there then from /etc/openldap/ldap.conf files.
Still if nothing is provided or found in the config files the command will exit out with a warning requesting the option be provided.

## Example Commands

After setting up the script to test you can try the following commands.
If you just want to lookup a user and see if they exist in the destination env you can run:

    $ ./bin/ldapmigrate uid=username lookup -m ldapserver.example.com -b dc=example,dc=com --password

or without any options (pr and using GSSAPI for authentication:

    $ kinit
    $ ./bin/ldapmigrate uid=username lookup

To migrate from on env to another use:

    $ ./bin/ldapmigrate uid=username migrate -m ldap.source.example.com -d ldap.dest.example.com -b dc=example,dc=com --password

or using GSSAPI authentication with only the required distination host option where the entry will be written (this should differ from the source host taken from the URI option in either the ~/.ldaprc file or /etc/openldap/ldap.conf ):

    $ kinit
    $ ./bin/ldapmigrate uid=username migrate -d ldapmaster.destination.example.com

## RFEs

Unable to migrate a container with multiple entries.
Would like automatic group membership modifications.



