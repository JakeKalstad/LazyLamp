import subprocess 
import os
import MySQLdb

print "___           ______      __      ___   __  __  _____"
print "| |          |___  /     | |     / _ \ |  \/  || ___ \\"
print "| |     __ _    / / _   _| |    / /_\ \| .  . || |_/ /"
print "| |    / _` |  / / | | | | |    |  _  || |\/| ||  __/"
print "| |___| (_| |./ /__| |_| | |____| | | || |  | || |"
print "\_____/\__,_|\_____/\__, \_____/\_| |_/\_|  |_/\_|"    
print "                     __/ |"
print "                    |___/"

def printer(cmd):
	 subprocess.check_call([cmd], shell=True)
	
def setup_mysql(pwd, oldpwd): 
	db = MySQLdb.connect("localhost","root",oldpwd,"mysql")
	cursor = db.cursor()
	cursor.execute("""UPDATE user SET Password=PASSWORD(%s) WHERE user='root'; FLUSH PRIVILEGES;""", pwd)

def install(installPhpFive, passwd, oldpwd):
	printer("apt-get update")
	if installPhpFive:
		printer("apt-get install apache2 php5 libapache2-mod-php5")
	else:
	    printer("apt-get install mysql-server mysql-client php4-mysql")
	setup_mysql(passwd, oldpwd)
	printer("apt-get install phpmyadmin")

def pollPhpVersion():
	phpVersion = raw_input("Php 4 or 5?\nversion:") 
	if phpVersion != "4" and phpVersion != "5":
 		return gatherVersion()
	return phpVersion

def write_config():
	configFile = open("/etc/apache2/apache2.conf", "a")
	configFile.write("#Include /etc/phpmyadmin/apache.conf")
	configFile.close()

oldpasswd = raw_input("Original MySql Password?(If any):")
passwd = raw_input("whats gonna be your MySqlPwd?\npassword:") 

install(pollPhpVersion(), passwd, oldpasswd)
write_config()
