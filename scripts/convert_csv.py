#!/usr/bin/python3
import csv

class host():
  count = 0
  layer = ""
  def __init__(self, use, name, alias, ipadd, hg, l):
    self.use = use
    self.name = name
    self.alias = alias
    self.address = ipadd
    self.group = hg
    self.layer = l
    #self.site = sn
    host.count += 1

def get_members_ingroup(g):
    s = ""
    for host in hosts_list:
        if host.group == g:
            s = host.name + ',' + s
    return s[:-1]

def get_hosts_inlayer(layer):
    s = ""
    for host in hosts_list:
        if host.layer == layer:
            s = host.name + ',' + s
    return s[:-1]

def get_floor_ap(s):
    st = s.split(".")
    if len(st) > 1 :
        if int(st[1])< 0:
            return st[1]
        elif int(st[1]) < 10 and int(st[1]) > 0:
            return '0'+st[1]
        else:
            return st[1]
    else:
        return "NA"  # Change for exit error

def get_name_sw(s):
    st = s.split(" ")

    if len(st) > 1 :
        return st[0]
        # if s[2] == "-":
        #     return s[0:5]
        # else:
        #     return s[0:4]
    else:
        return "NA"


def get_layer_sw(s):
    if len(s) > 1 :
        return s[0]+s[1]
    else:
        return "NA"

def get_floor_sw(s):
    if len(s) > 3 :
        if s[2] == "-":
            return s[2]+s[3]+s[4]
        else:
            return s[2]+s[3]
    else:
        return "NA"

def get_layer_si(s):
    st = s.split("_")
    if len(s) > 0 :
        return st[0]
    else:
        return "NA"

def get_floor_si(s):
    if len(s) > 1 :
        st = s.split("_")
        if st[0] == 'ISP':
            return "-" + st[1]
        else: return ""
    else:
        return ""

site = "Client001"
hosts_list = []

# Parse AP list
with open('csv/ap.csv') as csvData:
    next(csvData)
    file = csv.reader(csvData, delimiter=',',quoting= csv.QUOTE_ALL, quotechar = '"')
    for line in file:
        name = line[1]
        alias = line[0] # MAC
        address = line[3]
        layer = "Floor"  # Asume floor layer
        use = layer + "-host"
        group = line[12] + "-Floor-" + get_floor_ap(name) #Zone
        new_host = host(use, name, alias, address, group, layer)
        hosts_list.append(new_host)

print("####  Host count after ap list is: " + str(new_host.count))


# Parse SW list
with open('csv/sw.csv') as csvData:
    next(csvData)
    file = csv.reader(csvData, delimiter=',',quoting= csv.QUOTE_ALL, quotechar = '"')
    for line in file:
        name = get_name_sw(line[0])
        alias = line[1] # MAC
        ip_address = line[2]
        if get_layer_sw(name) != 'BB':
            layer = 'Floor'
            group = line[5] + '-' + layer + '-' + get_floor_sw(name)
        else:
            layer = get_layer_sw(name)
            group = line[5] + '-' + layer   #Zone
        use = layer +'-host'
        new_host = host(use, name, alias, ip_address, group, layer)
        hosts_list.append(new_host)

print("####  Host count after sw list is: " + str(new_host.count))

# Parse Site Inventory list
with open('csv/si.csv') as csvData:
    next(csvData)
    file = csv.reader(csvData, delimiter=',',quoting= csv.QUOTE_ALL, quotechar = '"')
    for line in file:
        name = line[0]
        alias = line[3] # MAC
        ip_address = line[2]
        if get_layer_si(name) == 'FW':
            layer = 'BB'
            group = line[4] + '-' + layer
        elif get_layer_si(name) == 'ISP':
            layer = 'ISP'
            group = line[4] + '-' + layer
        else:
            layer = 'IT' #get_layer_si(name)
            group = line[4] + '-' + layer + get_floor_si(name)

        use = layer +'-host'
        new_host = host(use, name, alias, ip_address, group, layer)
        hosts_list.append(new_host)

print("####  Host count in si list is: " + str(new_host.count))

## New configuration file
cfg = open(site +'.cfg', "w")

# Create hosts
for host in hosts_list:

    with open('templates/host.cfg', 'r') as file:
        data = file.read()

    data=data.replace('${use}', host.use)
    data=data.replace('${name}', host.name)
    data=data.replace('${alias}', host.alias)
    data=data.replace('${ip}', host.address)
    data=data.replace('${groups}', host.group)
    cfg.write(data)

# Create service
used_layers = []


for host in hosts_list:

    if host.layer not in used_layers:
        used_layers.append(host.layer)
        hosts_in_group = get_hosts_inlayer(host.layer)
        if hosts_in_group is not "":
            if host.layer == "FW":
                with open('templates/service.cfg', 'r') as file:
                    data = file.read()
            else:
                with open('templates/service.cfg', 'r') as file:
                    data = file.read()
            data=data.replace('${use}', host.use[:-4]+'service')
            data=data.replace('${names}', hosts_in_group)
        cfg.write(data)


# Create host_groups
used_groups = []

for host in hosts_list:
    print (host.name, host.group)
    if host.group not in used_groups:
        used_groups.append(host.group)
        members = get_members_ingroup(host.group)
        if members is not "":
            with open('templates/host_group.cfg', 'r') as file:
                data = file.read()
            data=data.replace('${name}', host.group)
            data=data.replace('${alias}', host.group)
            data=data.replace('${members}', members)
        cfg.write(data)


# Create internet layer


with open('templates/inet.cfg', 'r') as file:
    data = file.read()
data=data.replace('{Site_Name}', site)

cfg.write(data)

cfg.close()
