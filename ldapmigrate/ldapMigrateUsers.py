import ldap
import ldap.sasl
import ldap.modlist
import sys


class ldapMigrateUsers(object):

    def __init__(self, login="anonymous", ldap_host=None, ldap_base_dn=None, ldap_mod_host=None, password=None):
        #These will be used when args is added to the class assigning in the bin file
        self.ldap_base_dn = ldap_base_dn
        self.ldap_host = ldap_host
        self.ldap_mod_host = ldap_mod_host
        self.login = login
        self.auth = None
        if password:
            print "Not using GSSAPI"
            self.password = password
        else:
            print "using GSSAPI"
            self.auth = ldap.sasl.gssapi("")
    
            
    def list_attribs(self, search_entry):
        # def list_attribs(self, args):
        # self.login = login
        # self.auth = None
        # if password:
        #     print "Not using GSSAPI"
        #     self.password = password
        # else:
        #     print "using GSSAPI"
        #     self.auth = ldap.sasl.gssapi("")
        #These will be used when args is added to the class assigning in the bin file
        # self.ldap_base_dn = args.basedn
        # self.ldap_host = args.host
        # self.ldap_mod_host = args.mod_host
        # self.login = login
        # self.auth = None
        self.ldap_connection = ldap.initialize("ldap://" + self.ldap_host)
        self.ldap_connection.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/pki/tls/certs/newca.crt')
        self.ldap_connection.start_tls_s()
        if self.auth is None:
            print "Simple bind happening"
            self.ldap_connection.simple_bind_s("uid=" + self.login + ",ou=users," + self.ldap_base_dn, self.password)
        else:
            print "GSSAPI bind happening"
            self.ldap_connection.sasl_interactive_bind_s("", self.auth)
        self.search_entry = search_entry
        result = self.ldap_connection.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, search_entry)
        self.dn = result[0][0]
        self.result = result
        if len(result) == 0:
            print "User not found."
            sys.exit(1)
        else:
            return ldap.modlist.addModlist(result[0][1])
        self.ldap_connection.unbind()

    def migrate_user(self, search_entry):
        self.search_entry = search_entry
        self.entry = self.list_attribs(self.search_entry)
        #Calls the add_entry function
        self.add_entry()

    def lookup_user(self, args):
        if 'host' in args:
            LDAP_HOST = args.host
        if 'mod_host' in args:
            LDAP_MOD_HOST = args.mod_host
        LDAP_BASE_DN = args.basedn
        search_entry  = args.entry
        password = args.password[0]
        if 'lookup_host' in args:
            LDAP_HOST = args.lookup_host
        self.lookup_entry = search_entry
        # self.entry = self.list_attribs(args)
        self.entry = self.list_attribs(self.lookup_entry)
        print self.entry

    def add_entry(self, args):
        self.ldap_mod_conn = ldap.initialize("ldap://" + self.ldap_mod_host)
        self.ldap_mod_conn.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/pki/tls/certs/newca.crt')
        self.ldap_mod_conn.start_tls_s()
        if self.auth is None:
            print "Simple bind happening"
            self.ldap_mod_conn.simple_bind_s("uid=" + self.login + ",ou=users," + self.ldap_base_dn, self.password)
        else:
            print "GSSAPI bind happening"
            self.ldap_mod_conn.sasl_interactive_bind_s("", self.auth)
        self.dn = self.result[0][0]
        #print self.entry
        self.ldap_mod_conn.add_s(self.dn, self.entry)
        #print self.ldap_mod_conn.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, self.search_entry)
