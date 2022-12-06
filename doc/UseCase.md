# Server Connection Dashboard Use Cases

[TOC]

This doc will introduce the 2 use case of the Server Connection Dashboard. Currently the program has been used for one cyber exercise event and one academic infra service provider



------

### Use Case 1: CIDeX project



#### Project background

The inaugural Critical Infrastructure Defence Exercise (CIDeX) 2022 is the largest OT hands-on-keyboard Critical Infrastructure defence exercise. It provides a platform for Singapore’s cyber defenders to train together the defence of Critical Information Infrastructure (CII).With a better insight into how the CII – comprising IT and OT networks – can suffer from cyberattacks and their adverse consequences, the blue teams can distil these lessons and tailor them to augment their respective organisations’ cyber defence and protection strategies.

CIDeX 2022’s platform has three OT testbeds contributed by iTrust — the Secure Water Treatment (SWaT), Water Distribution (WaDi) and Electric Power and Intelligent Control (EPIC) OT testbeds, integrated with an Enterprise IT network of VMs hosted within NCL.Over 50 cyber defenders from 17 organisations representing five critical sectors — power, water, telecommunication, land transport and maritime — will form five combined blue teams to monitor and defend the CII systems over two days. A composite red team will launch a series of live simulated cyber attacks on these systems over two days, while the five blue teams will work in concert to detect and respond against the attacks.

A comprehensive 3-day pre-exercise training programme will be conducted in SAF’s Cyber Test and Evaluation Centre (CyTEC), so as to equip the blue teams with the capability and confidence to navigate through the CII platform and utilize appropriate cyber tools to monitor the platform and respond to the cyber attacks.



#### System config detail

As the event is hold in the NUS-COM3-MPH, so we need to monitor the connection latency from the MPH to the related peers and the internet. 

**Event day network ping latency monitor config**:

- Monitor time: 15/11/2022 8:30 am – 16/11/2022 6:30pm [34hours] 
- Monitor peers: 6 peers [4 public , 1 NUS internal, 1 VPN peer in SUTD]
- Ping Client Config: Ping each peer 5 times/min, report to hub every 1min. 
- Monitor hub alert threshold: 100 ms.
- Telegram-bot: update in Ncl-infra channel every 5min with 1 summary report.
- Entire ping latency chart during the 34 hours:

![](img/useCase1_1.JPG)

**Monitor server config:**

Running on backup DHCP server[192.168.127.11] , dashboard is accessible by any laptop/pc used in the event (connected to MPH network). 

![](img/useCase1_3.JPG)



------

### Use Case 2:  NCL OpenStack staging cluster connection monitor

As there are sever different kinds of academic infra server in the cluster such as SGX service, OpenStack servers and GPU server, we use the program to monitor different servers' connection simulation. 



![](img/useCase2_1.JPG)



------

