import ldap
import ldap.sasl
import ldap.modlist
import sys


class ldapMigrateUsers(object):

    def __init__(self, login="anonymous", ldap_host=None, ldap_base_dn=None, ldap_mod_host=None):
        self.ldap_base_dn = ldap_base_dn
        self.ldap_host = ldap_host
        self.ldap_mod_host = ldap_host
        self.auth = ldap.sasl.gssapi("")

    def list_attribs(self, search_user):
        self.ldap_connection = ldap.initialize("ldap://" + self.ldap_host)
        self.ldap_connection.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/pki/tls/certs/newca.crt')
        self.ldap_connection.start_tls_s()
        self.ldap_connection.sasl_interactive_bind_s("", self.auth)
        self.search_user = search_user
        print self.search_user
        result = self.ldap_connection.search_s("ou=Users," + self.ldap_base_dn, ldap.SCOPE_SUBTREE, "uid=" + search_user)
        print result
        user2 = result[0]
        self.result = result
        print "checking user2"
        print user2
        print user2[1]['uid']
        print "################"
        user_3 = user2[1]['uid'] #this creates a one entry list
        print user_3[0] #this basically makes the list into a string of the uid
        if len(result) == 0:
            print "User not found."
            sys.exit(1)
        else:
            return ldap.modlist.addModlist(result[0][1])
        self.ldap_connection.unbind()
#            print data_l

#        except ldap.LDAPError, e:
#            print e


    # l = ldap.initialize('ldap://ldap.example.com',trace_level=1)
    # attrib_list = []
    # for entry in x:
    #     attrib_dict = entry[1]
    #     for a in attrib:
    #         out = '%s: %s'
    #         print out.format(a, attrib_dict[a])
    #         attrib_list.append(out)
    #         print attrib_list
    #         return attrib_list

    def migrate_user(self, search_user):
        self.search_user = search_user
        self.entry = self.list_attribs(self.search_user)
        print self
        self.add_user()

    def add_user(self):
        self.ldap_mod_conn = ldap.initialize("ldap://" + self.ldap_mod_host)
        self.ldap_mod_conn.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/pki/tls/certs/newca.crt')
        self.ldap_mod_conn.start_tls_s()
        self.ldap_mod_conn.sasl_interactive_bind_s("", self.auth)
        print "The dn of the user"
        self.dn = self.result[0][0]
        print self.dn
        print "The entry that is going to be added"
        print self.entry
        #self.ldap_mod_conn.add_s(self.dn, self.entry,)

#         try:
#             self.ldap_connection = ldap.initialize('ldap.example.com')
# #            auth = ldap.sasl.gssapi("")
#             if login == "anonymous":
#                 self.ldap_connection.simple_bind_s("", "")
#             else:
#                 self.ldap_connection.start_tls_s()
#                 # authenticate with kerberos
#                 self.ldap_connection.sasl_interactive_bind_s("", auth)
# #                ldap.set_option(ldap.OPT_X_TLS_CACERT,'/etc/openldap/cacerts/newca.crt')
#         except ldap.LDAPError, e:
#             sys.stderr.write("Fatal LDAP Error.\n")
#             sys.stderr.write("Error: %sn" % e);
#             print "\nBye."
#             sys.exit()
