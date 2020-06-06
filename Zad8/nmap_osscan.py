from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
import pandas as pd

IP_ADDR = '192.168.1.'

nm = NmapProcess(IP_ADDR + '0/24', options="-O")

rc = nm.run()

if nm.rc == 0:
    #nmap_report = NmapParser.parse_fromfile('OS_scan.xml')
    nmap_report = NmapParser.parse(nm.stdout)

    print("Nmap scan summary: {}".format(nmap_report.summary))

    host_names = list()
    addr_list = list()
    os_list = list()
    acc_list = list()

    for host in nmap_report.hosts:
        matched_os = host.os_class_probabilities()
        if len(host.hostnames) > 0 and len(matched_os) > 0:
            host_names.append(host.hostnames[0])
            addr_list.append(host.address)
            os_list.append(matched_os[0].description)
            acc_list.append(matched_os[0].accuracy)

    dict = {'Name': host_names, 'IP': addr_list,'OS': os_list,'Accuracy [%]': acc_list}
    df = pd.DataFrame(dict)
    print(df)

    df.to_csv('scan_results.csv', index=False)
else:
    print(nm.stderr)

