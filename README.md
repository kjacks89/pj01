#CS 4760 pj01
Kyle Jackson 811-249-956

##Description

This is a simple concurrent server implementing the HTTP/1.1 protocol and uses the low-level socket networking interface.

##Instructions
To run the program, go into my cs4760 directory and ssh into a cluster node 
(e.g. vcf0 or vcf3).

Then activate the virtual environment by typing:
$ source pj01/bin/activate

Go into the hw01 directory and run the server by typing:
$ python3 

Go into different nike session/s (in different terminals) and type in
the following command:
telnet <cluster> 47656
The 47656 is my port number used in the knock_knock_server.py class. Do not 
include the greater than/less than symbols in the above command, just type the
actual cluster name.

##Attribution
~            
