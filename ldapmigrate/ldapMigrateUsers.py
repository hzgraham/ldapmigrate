import ldap
import ldap.sasl
import ldap.modlist
import sys


class ldapMigrateUsers(object):

    def __init__(self, login="anonymous", ldap_host=None, ldap_base_dn=None, ldap_mod_host=None, password=None):
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
                print self.auth

    def list_attribs(self, search_entry):
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
        print self.search_entry
        result = self.ldap_connection.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, search_entry)
        print result
        self.dn = result[0][0]
        self.result = result
        print "################"
        if len(result) == 0:
            print "User not found."
            sys.exit(1)
        else:
            return ldap.modlist.addModlist(result[0][1])
        self.ldap_connection.unbind()

    def migrate_user(self, search_entry):
        print "Doing stuff in migrate_user function"
        self.search_entry = search_entry
        self.entry = self.list_attribs(self.search_entry)
        print self.entry
        #print self.dn
        self.add_user()

    def lookup_user(self, search_entry):
        self.lookup_entry = search_entry
        self.entry = self.list_attribs(self.lookup_entry)
        print self.dn
        print self.entry
        #print self.dn

    def add_user(self):
        self.ldap_mod_conn = ldap.initialize("ldap://" + self.ldap_mod_host)
        self.ldap_mod_conn.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/pki/tls/certs/newca.crt')
        self.ldap_mod_conn.start_tls_s()
        print self.auth
        print "This is the DN of the user: ",self.dn
        if self.auth is None:
            print "Simple bind happening"
            self.ldap_mod_conn.simple_bind_s("uid=" + self.login + ",ou=users," + self.ldap_base_dn, self.password)
        else:
            print "GSSAPI bind happening"
            self.ldap_mod_conn.sasl_interactive_bind_s("", self.auth)
        self.dn = self.result[0][0]
        #print self.entry
        self.ldap_mod_conn.add_s(self.dn, self.entry)
        print self.ldap_mod_conn.search_s( self.ldap_base_dn, ldap.SCOPE_SUBTREE, self.search_entry)
