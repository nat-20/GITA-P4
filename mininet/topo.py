#!/usr/bin/python

#  Copyright 2019-present Open Networking Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Host
from mininet.topo import Topo

from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.node import CPULimitedHost

import sys

sys.path.insert(0, '~/ngsdn-tutorial/mininet')
from stratum_new import StratumBmv2Switch

CPU_PORT = 255


class TutorialTopo(Topo):
    """2x2 fabric topology with IPv4 hosts"""

    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        # Leaves

        # gRPC port 50001
        s1 = self.addSwitch('s1', cls=StratumBmv2Switch, cpuport=CPU_PORT)

        # IPv4 hosts attached to S1
        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip='10.0.0.1/24') #, gw='10.0.0.254')
        self.addLink(s1, h1)  #Port 1

        # IPv4 hosts attached to S2
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip='10.0.0.2/24') #, gw='10.0.0.254')
        self.addLink(s1, h2)  #Port 2


def main():
	net = Mininet(topo=TutorialTopo(), controller=None, link=TCLink)#, switch=OVSKernelSwitch)
	net.staticArp() #Avoiding ARP process
	net.start()
	CLI(net)
	net.stop()
	print '#' * 80
	print 'ATTENTION: Mininet was stopped! Perhaps accidentally?'
	print 'No worries, it will restart automatically in a few seconds...'
	print 'To access again the Mininet CLI, use `make mn-cli`'
	print 'To detach from the CLI (without stopping), press Ctrl-D'
	print 'To permanently quit Mininet, use `make stop`'
	print '#' * 80


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Mininet topology script for 2x2 fabric with stratum_bmv2 and IPv4 hosts')
    args = parser.parse_args()
    setLogLevel('info')

    main()
