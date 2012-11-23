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
def GenNat(WANAddr,LANNet,WANInt,LANInt):
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
	print "place holder"

#start	
if __name__ == "__main__":
    main()