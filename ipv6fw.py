#!/usr/bin/python
import sys
import json

def GenFW(wan_int, lan_int):
	"""                                                           
	FUNCTION NAME: GenNat
	INPUTS: wan_addr lan_net, lan_mask, wan_int, lan_int
	OUTPUTS: IP Tables commands in a string
	NOTES: Generates the NAT components for IPv4

	"""
	commands = [
		'sysctl -w net.ipv6.conf.all.forwarding=1',
		'ip6tables -P INPUT DROP',
		'ip6tables -A INPUT -i %(lan_int)s -j ACCEPT',
		'ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT',
		'ip6tables -A INPUT -i %(wan_int)s -p icmpv6 -j ACCEPT',
		'ip6tables -P FORWARD DROP',
		'ip6tables -A FORWARD -i %(lan_int)s -o %(wan_int)s -j ACCEPT',
		'ip6tables -A FORWARD -i %(wan_int)s -o %(lan_int)s -p icmpv6 -j ACCEPT',
		'ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT'
		]
	command = '\n'.join(commands)
	return command % locals()

def GenPortMap(ip,proto,port):
	"""
	FUNCTION NAME: GenPortMap
	INPUTS: externalPort, internalPort, interalIP, protocol
	OUTPUTS: 2 ip6tables lines representing a port map
	NOTES: Opens a port on the FORWARD and INPUT table for a specific IP
	"""
	commands = [
	'ip6tables -I INPUT -d %(ip)s -p %(proto)s --dport %(port)s -j ACCEPT',
	'ip6tables -I FORWARD -d %(ip)s -p %(proto)s --dport %(port)s -j ACCEPT',
	]
	command = '\n'.join(commands)
	return command % locals()

def GenOpenPort(port,proto,int):
	"""                                                         
	FUNCTION NAME: GenOpenPort
	INPUTS: port, protocol, interface
	OUTPUTS: IP tables command to open a port on an interface
	NOTES: Opens a port on an interface. Warning: this will open the port for only the INPUT table.

	Sample output
	iptables -I INPUT -i eth0 -p udp --dport 161 -j ACCEPT
	"""
	command = 'ip6tables -I INPUT -i %(int)s -p %(proto)s --dport %(port)s -j ACCEPT'
	return command % locals()


def main():
	"""                                                 
	FUNCTION NAME: Main
	INPUTS: commandline variables
	OUTPUTS: Firewall Script
	NOTES: main routine, generates the firewall script 
	"""

	#debug code
	

	print GenFW("ppp0", "eth0")
	print GenOpenPort("4500","tcp","ppp0")
	
	fw6_settings_file = open ('conf/fw6_settings.json','rb')
	port_maps_file = open ('conf/port_maps6.json','rb')
	open_ports_file = open ('conf/open_ports6.json','rb')


	print '#!/bin/bash'	

	fw6_settings_json = json.loads(fw6_settings_file.read())
	print GenFW(fw6_settings_json["wan_int"],fw6_settings_json["lan_int"])
			
	port_maps_json = json.loads(port_maps_file.read())
	for port_maps in port_maps_json["port_maps"]:
		print GenPortMap(port_maps["port"],port_maps["ip"],port_maps["proto"])	
	
	open_ports_json = json.loads(open_ports_file.read())
	for open_ports in open_ports_json["open_ports"]:
		print GenOpenPort(open_ports["port"],open_ports["proto"],open_ports["int"])



#start	
if __name__ == "__main__":
    main()
