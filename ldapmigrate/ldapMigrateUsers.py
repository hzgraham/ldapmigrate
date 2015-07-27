import ldap
import ldap.sasl
import ldap.modlist
import sys
import os

class ldapMigrateUsers(object):

    def __init__(self, login="anonymous", ldap_host=None, ldap_base_dn=None, ldap_mod_host=None, password=None):
        #These will be used when args is added to the class assigning in the bin file
        self.ldap_mod_host = ldap_mod_host
        self.login = login
        self.auth = None
        self.homedir = os.getenv("HOME")
        self.ldaprc = self.homedir+'/.ldaprc'
        self.ldapconf = '/etc/openldap/ldap.conf'

    def get_config_option(self, option):
        if os.path.exists(self.ldaprc):
            with open(self.ldaprc, 'r') as myfile:
                lines = myfile.readlines()
                for line in lines:
                    if line != "\n" and not line.startswith('#'):
                        if line.startswith(option):
                            return line.split()[1].strip()
        elif os.path.exists(self.ldapconf):
            with open(self.ldapconf, 'r') as myfile:
                lines = myfile.readlines()
                for line in lines:
                    if line != "\n" and not line.startswith('#'):
                        if line.startswith(option):
                            return line.split()[1].strip()

    def list_attribs(self, args):
        self.cacertdir = None
        self.cacertfile = None
        #login="anonymous"
        if args.lookup_host:
            self.ldap_host = args.lookup_host
        else:
            option = 'URI'
            self.ldap_host = self.get_config_option(option)
        if not self.ldap_host:
            sys.exit('Please Specify a '+option+'!')
        if 'mod_host' in args:
            LDAP_MOD_HOST = args.mod_host
        if args.basedn:
            self.ldap_base_dn = args.basedn
        else:
            option = 'BASE'
            self.ldap_base_dn = self.get_config_option(option)
        if not self.ldap_base_dn:
            sys.exit('Please Specify a '+option+'!')
        if args.cacert:
            self.cacert = args.cacert
        else:
            option_file = 'TLS_CACERT'
            option_dir = 'TLS_CACERTDIR'
            self.cacert_file = self.get_config_option(option_file)
            self.cacert_dir = self.get_config_option(option_dir)
            if self.cacert_dir:
                self.cacertdir = self.cacert_dir
            elif self.cacert_file:
                self.cacertfile = self.cacert_file
            else:
                sys.exit('Please Specify a CA cert file or directory!')
        self.auth = None
        self.search_entry  = args.entry
        if args.password:
            password = args.password[0]
            print "Not using GSSAPI"
            self.password = password
        else:
            self.auth = ldap.sasl.gssapi("")
        if self.ldap_host.startswith('ldap://'):
            self.ldap_connection = ldap.initialize(self.ldap_host)
        else:
            self.ldap_connection = ldap.initialize("ldap://" + self.ldap_host)
        if self.cacertdir:
            self.ldap_connection.set_option(ldap.OPT_X_TLS_CACERTDIR,self.cacertdir)
        elif self.cacertfile:
            self.ldap_connection.set_option(ldap.OPT_X_TLS_CACERTFILE,self.cacertfile)
        if self.auth is None:
            print "Simple bind happening"
            self.ldap_connection.start_tls_s()
            self.ldap_connection.simple_bind_s("uid=" + self.login + ",ou=users," + self.ldap_base_dn, self.password)
        else:
            print "GSSAPI bind happening"
            self.ldap_connection.sasl_interactive_bind_s("", self.auth)
        result = self.ldap_connection.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, self.search_entry)
        #self.dn = result[0][0]
        self.result = result
        print self.result
        #Checks if the returned entry is empty
        if len(result) == 0:
            print "Entry not found."
            sys.exit(1)
        else:
            #print ldap.modlist.addModlist(result[0][1])
            return ldap.modlist.addModlist(result[0][1])
        self.ldap_connection.unbind()

    def migrate_user(self, args):
        self.entry = self.list_attribs(args)
        #Calls the add_entry function
        self.add_entry(args)

    def add_entry(self, args):
        self.ldap_mod_conn = ldap.initialize("ldap://" + self.ldap_mod_host)
        if self.cacertdir:
            self.ldap_mod_conn.set_option(ldap.OPT_X_TLS_CACERTDIR,self.cacertdir)
        elif self.cacertfile:
            self.ldap_mod_conn.set_option(ldap.OPT_X_TLS_CACERTFILE,self.cacertfile)
        self.ldap_mod_conn.start_tls_s()
        if self.auth is None:
            print "Simple bind happening"
            self.ldap_mod_conn.simple_bind_s("uid=" + self.login + ",ou=users," + self.ldap_base_dn, self.password)
        else:
            print "GSSAPI bind happening"
            self.ldap_mod_conn.sasl_interactive_bind_s("", self.auth)
        self.dn = self.result[0][0]
        self.ldap_mod_conn.add_s(self.dn, self.entry)
        #print self.ldap_mod_conn.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, self.search_entry)
