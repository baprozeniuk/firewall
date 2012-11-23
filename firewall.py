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
##
##
##
###################################################################
def GenNat(WANAddr,LANNet,WANInt,LANInt):
	return nat

###################################################################
##                                                               
##        FUNCTION NAME: GenPortMap
##        INPUTS: externalPort, internalPort, interalIP, protocol
##        OUTPUTS: portMap
##        NOTES: Generates an iptables port map
##
##
##
###################################################################
def GenPortMap(extPort,intPort,intIP,proto):
	return map
###################################################################
##                                                               
##        FUNCTION NAME: GenOpenPort
##        INPUTS: port, protocol
##        OUTPUTS: opens a port to the router
##        NOTES:
##
##
##
###################################################################.
def GenOpenPort(port,proto):
	return port
###################################################################
##                                                               
##        FUNCTION NAME: GenStaticNetRoute
##        INPUTS: network, netmask, gateway
##        OUTPUTS: commandline to add a static route
##        NOTES: Adds a static route to the script
##
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