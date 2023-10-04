from ldap3 import Server, Connection, ALL, NTLM
import getpass

#-1 if server denied
#0 if account denied
#1 if logged in
def login(username, password):
    if username == None or password == None:
        return -1

    server = Server("chrome.wiregrass.edu", get_info=ALL)
    conn = Connection(server, user="wiregrass\\" + username, password=password, authentication=NTLM)

    try:
        conn.bind()
    except:
        print("-1: Could not bind to server")
        return -1

    who = conn.extend.standard.who_am_i()

    if str(who)[0] == "u":
        print("1: Access approved")
        return 1
    else:
        print("0: Access denied")
        return 0

    return 0
