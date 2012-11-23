###################################################################
##                                                               
##        FUNCTION NAME:
##        INPUTS:
##        OUTPUTS: 
##        NOTES:
##
##
##
###################################################################

import sys


###################################################################
##                                                               
##        FUNCTION NAME: GenNat
##        INPUTS: WANAddr, LANNet, WANInt, LANInt
##        OUTPUTS: NATScript
##        NOTES: Generates the NAT components for IPv4
##Sample output, with bash variables. should be different output from this
"""
sysctl -w net.ipv4.ip_forward=1 #enable fowarding
iptables -P FORWARD ACCEPT
iptables -F FORWARD 

#FWD: Allow all connections OUT and only existing and related ones IN
iptables -A FORWARD -i $WANINTERFACE -o $LANINTERFACE -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i $LANINTERFACE -o $WANINTERFACE -j ACCEPT

iptables -t nat -A POSTROUTING -s 10.0.0.0/8 -o $WANINTERFACE -j SNAT --to-source $WANADDRESS
iptables -I POSTROUTING -t nat -o $WANINTERFACE -d $WANADDRESS/24 -j MASQUERADE
"""
###################################################################
def GenNat(WANAddr,WANMask,LANNet,LANMask,WANInt,LANInt):
	nat = "sysctl -w net.ipv4.ip_forward=1\n"
	nat += "iptables -P FORWARD ACCEPT\n"
	nat += "iptables -F FORWARD\n"
	nat += "iptables -A FORWARD -i " + WANInt + " -o " + LANInt + " -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
	nat += "iptables -A FORWARD -i " + LANInt + " -o " + WANInt + " -j ACCEPT\n"
	nat += "iptables -t nat -A POSTROUTING -s " + LANNet + "/" + LANMask + " -o " + WANInt + " -j SNAT --to-source " + WANAddr + "\n"
	nat += "iptables -I POSTROUTING -t nat -o " + WANInt + " -d " + WANAddr + "/" + WANMask + " -j MASQUERADE\n"
	return nat

###################################################################
##                                                               
##        FUNCTION NAME: GenPortMap
##        INPUTS: externalPort, internalPort, interalIP, protocol
##        OUTPUTS: portMap
##        NOTES: Generates an iptables port map
##Results should look like
"""
iptables -t nat -I PREROUTING -p tcp --dport 45678 -j DNAT --to 10.60.0.3:45678
iptables -I FORWARD -p tcp -d 10.60.0.3 --dport 45678 -j ACCEPT
"""
##
###################################################################
def GenPortMap(extPort,intPort,intIP,proto):
	map = "iptables -t nat -I PREROUTING -p " + proto + " --dport " + extPort + " -j DNAT --to " + intIP + ":" + intPort +"\n"
	map += "iptables -I FORWARD -p " + proto + " -d " + intIP + " --dport " + intPort + " -j ACCEPT\n" 
	return map
###################################################################
##                                                               
##        FUNCTION NAME: GenOpenPort
##        INPUTS: port, protocol,extInt
##        OUTPUTS: opens a port to the router
##        NOTES:
##
##Sample output
"""
iptables -I INPUT -i eth0 -p udp --dport 161 -j ACCEPT
"""
##
###################################################################.
def GenOpenPort(port,proto,extInt):
	port = "iptables -I INPUT -i " + extInt + " -p " + proto + " --dport " + port + " + -j ACCEPT\n"
	return port
###################################################################
##                                                               
##        FUNCTION NAME: GenStaticNetRoute
##        INPUTS: network, netmask, gateway
##        OUTPUTS: commandline to add a static route
##        NOTES: Adds a static route to the script
##Sample Output
"""
route add -net 10.9.9.0/24 gw 10.66.12.1
"""
##
##
###################################################################
def GenStaticNetRoute(net,mask,gw):
	route = "route add -net " + net + "/" + mask + " gw " + gw + "\n"
	return route

###################################################################
##                                                               
##        FUNCTION NAME: Main
##        INPUTS: commandline variables
##        OUTPUTS: Firewall Script
##        NOTES: main routine, generates the firewall script 
##
##
##
###################################################################
def main():
	print "#nat"
	print GenNat("95.211.129.156","32","10.0.0.0","8","eth0","eth1")
	print "#Port map"
	print GenPortMap("4500","4500","10.9.9.50","tcp")
	print "#OpenPort"
	print GenOpenPort("5900","tcp","eth0")
	print "#Static Route"
	print GenStaticNetRoute("10.9.9.0","24","10.66.12.1")
#start	
if __name__ == "__main__":
    main()