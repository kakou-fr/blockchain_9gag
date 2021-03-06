import sys
import binascii

from Savoir import Savoir
import ipfsapi

# except:
# print("You need to install ipfs and/or Savoir, see googledocs instructions")
# sys.exit(-1)


def resolve_name(account):
    #ajouter prise en compte du plus recent
    nicknames = apirpc.liststreamitems('nickname_resolve')
    ret = 'name not found'
    for nickname in nicknames:
        if nickname['publishers'][0] == account:
            if nickname['key'] == 'pseudo':
                ret = binascii.unhexlify(nickname['data'])
    return ret


if len(sys.argv) < 2:
    print("Usage: <chain>")
    sys.exit(-1)

chainname = str(sys.argv[1])
pathconf = "/root/.multichain/" + chainname + "/multichain.conf"
rpcuser = ""
rpcpassword = ""

with open("/root/.multichain/chain1/multichain.conf", "r") as f:
    line_list = [c for c in f.readlines()]
    for line in line_list:
        if "rpcuser=" in line:
            rpcuser = line.split("=")[1]
        elif "rpcpassword=" in line:
            rpcpassword = line.split("=")[1]
    if rpcuser == "":
        print("Couldn't retrieve rpcuser from " + chainname)
        sys.exit(-1)
    elif rpcpassword == "":
        print("Couldn't retrieve rpcpassword from " + chainname)
        sys.exit(-1)

rpcuser = rpcuser.replace('\n', '')
rpcpassword = rpcpassword.replace('\n', '')

rpchost = '127.0.0.1'
rpcport = '1235'

apirpc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
# on se connecte au noeud IPFS
api = ipfsapi.connect('127.0.0.1', 5001)

# on ajoute le fichier
s = apirpc.liststreams()
streams = []
for i in s:
    if i['name'] != 'root' and i['name'] != 'default_account' and i['name'] != 'nickname_resolve':
        streams.append(i['name'])

posts = []
for item in streams:
    stream = apirpc.liststreamitems(item)
    nom = binascii.unhexlify(item)
    ipfs = ''
    type_contenu = ''
    author_account = ''
    smartAddr = ''
    for it in stream:
        if it['key'] == 'ipfs':
            ipfs = binascii.unhexlify(it['data'])
            author_account = it['publishers'][0]
        if it['key'] == 'type':
            type_contenu = binascii.unhexlify(it['data'])
        if it['key'] == 'smartcontract':
            smartAddr = binascii.unhexlify(it['data']) 
    if ipfs != '' and type_contenu != '' and author_account != '':
        author = resolve_name(author_account)
        posts.append({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author, 'smartcontract': smartAddr})

print(posts)
for item in posts:
    print(item['title'])
    print(item['type'])
    print(item['author'])
    print(item['smartcontract'])
    #print(api.cat(item['ipfs']))
    print('https://ipfs.io/ipfs/' + item['ipfs'])
