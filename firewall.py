#!/usr/bin/python
import sys
import json

def GenNat(wan_addr, lan_net, lan_mask, wan_int, lan_int):
	"""                                                           
	FUNCTION NAME: GenNat
	INPUTS: wan_addr lan_net, lan_mask, wan_int, lan_int
	OUTPUTS: IP Tables commands in a string
	NOTES: Generates the NAT components for IPv4

	Sample output, with bash variables. should be different output from this

	sysctl -w net.ipv4.ip_forward=1 #enable fowarding
	iptables -P FORWARD ACCEPT
	iptables -F FORWARD 

	#FWD: Allow all connections OUT and only existing and related ones IN
	iptables -A FORWARD -i $WANINTERFACE -o $LANINTERFACE -m state --state ESTABLISHED,RELATED -j ACCEPT
	iptables -A FORWARD -i $LANINTERFACE -o $WANINTERFACE -j ACCEPT

	iptables -t nat -A POSTROUTING -s 10.0.0.0/8 -o $WANINTERFACE -j SNAT --to-source $WANADDRESS
	iptables -I POSTROUTING -t nat -o $WANINTERFACE -d $WANADDRESS -j MASQUERADE
	"""
	commands = [
		'sysctl -w net.ipv4.ip_forward=1',
		'iptables -P FORWARD ACCEPT',
		'iptables -F FORWARD',
		'iptables -A FORWARD -i %(wan_int)s  -o %(lan_int)s -m state --state ESTABLISHED,RELATED -j ACCEPT',
		'iptables -A FORWARD -i %(lan_int)s -o %(wan_int)s -j ACCEPT',
		'iptables -t nat -A POSTROUTING -s %(lan_net)s/%(lan_mask)s -o %(wan_int)s -j SNAT --to-source %(wan_addr)s',
		'iptables -I POSTROUTING -t nat -o %(wan_int)s -d %(wan_addr)s -j MASQUERADE',
		]
	command = '\n'.join(commands)
	return command % locals()

def GenPortMap(ext_port,int_port,int_ip,proto):
	"""
	FUNCTION NAME: GenPortMap
	INPUTS: externalPort, internalPort, interalIP, protocol
	OUTPUTS: 2 iptables lines representing a port map
	NOTES: Generates an iptables port map
	Sample Output

	iptables -t nat -I PREROUTING -p tcp --dport 45678 -j DNAT --to 10.60.0.3:45678
	iptables -I FORWARD -p tcp -d 10.60.0.3 --dport 45678 -j ACCEPT
	"""
	commands = [
	'iptables -t nat -I PREROUTING -p %(proto)s --dport %(ext_port)s -j DNAT --to %(int_ip)s:%(int_port)s',
	'iptables -I FORWARD -p %(proto)s -d %(int_ip)s --dport %(int_port)s -j ACCEPT',
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
	command = 'iptables -I INPUT -i %(int)s -p %(proto)s --dport %(port)s -j ACCEPT'
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
	"""
	#debug code
	print "#nat"
	print GenNat("95.211.129.156","10.0.0.0","8","eth0","eth1")
	print "#Port map"
	print GenPortMap("4500","4500","10.9.9.50","tcp")
	print "#OpenPort"
	print GenOpenPort("5900","tcp","eth0")
	print "#Static Route"
	print GenStaticNetRoute("10.9.9.0","24","10.66.12.1")
	"""
	nat_settings_file = open ('conf/nat_settings.json','rb')
	port_maps_file = open ('conf/port_maps.json','rb')
	static_routes_file = open ('conf/routes.json','rb')
	open_ports_file = open ('conf/open_ports.json','rb')


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
#start	
if __name__ == "__main__":
    main()
