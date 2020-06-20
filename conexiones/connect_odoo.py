import xmlrpc.client
# info = xmlrpc.client.ServerProxy('https://smsconsulting.ec').start()
# url, db, username, password = \
#     info['host'], info['database'], info['user'], info['password']

url = "https://itsgg.manexware.com"
db = "itsgg"
username = "admin"
password = "Admin123*"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# print(common.version())