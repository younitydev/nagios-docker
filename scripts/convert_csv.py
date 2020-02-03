import csv
import numpy as np
#cfg = __dict__

#layers = ['sfloor', 'ISP', 'BB', 'IT', 'internet']

# parse AP list

hosts_list = []

with open('ap.csv') as csvData:
    file = csv.reader(csvData)
    for line in file:
        ap_name = line[1]
        ap_mac = line[0]
        ip_address = line[3]
        zone = line[13]
        #layer = 'floor'+ get_floor_number(ap_name)
        #host.use = layer+'host'
        host.name = ap_name
        host.alias = ap_mac
        host.address = ip_address
        #host.hostgroups = zone + “_” + layer
        #host_list.append(host)
        host_list = np.append(host_list,host)
        print (line)

#hosts[i]

hosts_list = append(host)


#parse switch list

#switchName,macAddress,ipAddress,firmwareVersion,status,groupName,model,firmwareUpdate,upTime,ports,portStatus,registrationStatus,alarm,poe,serialNumber,lastBackupTime
#BB02 (01) (),D4:C1:9E:0C:1D:80,172.16.0.73,,ONLINE,Sapir,,N/A,,52,26 2 26,APPROVED,1,0/0 watt,CYS3331P014,1.57957E+12


# host_name = switchName
# alias = macAddress
# ipddress = ipAddress
# hostgroups = groupName + “_” + Layer
#
#
# services
# hosts
# host_groups
#
#
#
#         print(row)
#
#
# # parse Devices list
