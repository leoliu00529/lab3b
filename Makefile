# NAME: Yuan Shen, Zihan Liu
# EMAIL: yuanshen@g.ucla.edu, leoliu00529@gmail.com
# ID: 605142505, 105144205

TARBALL= lab3b-605142505.tar.gz
CFLAG= -Wall -Wextra -g

default:	
	rm -f lab3b
	ln lab3b_temp.sh lab3b
	chmod +rwx lab3b

clean:
	rm -f *.tar.gz lab3b

dist:   
	tar -cvzf $(TARBALL) README Makefile lab3b_temp.sh lab3b.py
