#!/usr/bin/python
import sys
import json

def GenFW(lan_net, lan_mask, wan_int, lan_int):
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

def GenPortMap(ext_port,int_port,int_ip,proto):
	"""
	FUNCTION NAME: GenPortMap
	INPUTS: externalPort, internalPort, interalIP, protocol
	OUTPUTS: 2 ip6tables lines representing a port map
	NOTES: Generates an iptables port map
	Sample Output


	"""
	commands = [
	'',
	'',
	]
	command = '\n'.join(commands)
	return command % locals()

def GenOpenPort(port,proto,int):
	"""                                                         
	FUNCTION NAME: GenOpenPort
	INPUTS: port, protocol, interface
	OUTPUTS: IP tables command to open a port on an interface
	NOTES: Opens a port on an interface

	Sample output
	iptables -I INPUT -i eth0 -p udp --dport 161 -j ACCEPT
	"""
	command = 'ip6tables -I INPUT -i %(int)s -p %(proto)s --dport %(port)s -j ACCEPT'
	return command % locals()


def GenStaticNetRoute(net,mask,gw):
	"""                                                       
	FUNCTION NAME: GenStaticNetRoute
	INPUTS: network, netmask, gateway
	OUTPUTS: commandline to add a static route
	NOTES: Adds a static route to the script
	Sample Output

	route add -net 10.9.9.0/24 gw 10.66.12.1
	"""
	command = 'route add -net %(net)s/%(mask)s gw %(gw)s'
	return command % locals()


def main():
	"""                                                 
	FUNCTION NAME: Main
	INPUTS: commandline variables
	OUTPUTS: Firewall Script
	NOTES: main routine, generates the firewall script 
	"""

	#debug code
	

	print GenFW("2001:1AF8:4600:A009:0001::", 64, "ppp0", "eth0")
	print GenOpenPort("4500","tcp","ppp0")
	"""
	nat_settings_file = open ('conf/fw6_settings.json','rb')
	port_maps_file = open ('conf/port_maps6.json','rb')
	static_routes_file = open ('conf/routes6.json','rb')
	open_ports_file = open ('conf/open_ports6.json','rb')


	print '#!/bin/bash'	

	nat_settings_json = json.loads(nat_settings_file.read())
	print GenNat(nat_settings_json["wan_addr"],nat_settings_json["lan_net"],nat_settings_json["lan_mask"],nat_settings_json["wan_int"],nat_settings_json["lan_int"])
			
	port_maps_json = json.loads(port_maps_file.read())
	for port_maps in port_maps_json["port_maps"]:
		print GenPortMap(port_maps["ext_port"],port_maps["int_port"],port_maps["int_ip"],port_maps["proto"])	
	
	open_ports_json = json.loads(open_ports_file.read())
	for open_ports in open_ports_json["open_ports"]:
		print GenOpenPort(open_ports["port"],open_ports["proto"],open_ports["int"])
	
	static_routes_json = json.loads(static_routes_file.read())
	for routes in static_routes_json["routes"]:
		print GenStaticNetRoute(routes["net"],routes["mask"],routes["gw"])
"""

#start	
if __name__ == "__main__":
    main()
