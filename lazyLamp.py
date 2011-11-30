import subprocess 
import os
import sys
import MySQLdb
import wx

print "___           ______      __      ___   __  __  _____"
print "| |          |___  /     | |     / _ \ |  \/  || ___ \\"
print "| |     __ _    / / _   _| |    / /_\ \| .  . || |_/ /"
print "| |    / _` |  / / | | | | |    |  _  || |\/| ||  __/"
print "| |___| (_| |./ /__| |_| | |____| | | || |  | || |"
print "\_____/\__,_|\_____/\__, \_____/\_| |_/\_|  |_/\_|"    
print "                     __/ |"
print "                    |___/"

"""
  
"""
class CLIModel:
	def get_old_mysql_pwd(self):
		return raw_input("Original MySql Password?(If any)\npassword:")
	def get_new_mysql_pwd(self):
		return raw_input("whats gonna be your MySqlPwd?\npassword:") 
	def get_php_version(self):
		phpVersion = raw_input("Php 4 or 5?\nversion:") 
		if phpVersion != "4" and phpVersion != "5":
	 		return get_php_version(self)
		return phpVersion

## GLOBALZ

def exit_route():
	sys.exit("\nMust provide a choice of ui, either c(CLI) or w(wXWidgets)\n\to.O\n  example: python lazyLamp.py c")
	
def call(cmd):
	 subprocess.check_call([cmd], shell=True)

######### WX MODE 
class WxLampApp(wx.App): 
    def __init__(self, parent, model):
	self.model = model 
	wx.App.__init__(self, parent)

    def OnInit(self): 
        frame = MainGui(None, -1, "Lazy LAMP", self.model)
        frame.Show(True) 
        self.SetTopWindow(frame) 
        return True
 
class MainGui(wx.Frame):
    def __init__(self, parent, id, title, model): 
        wx.Frame.__init__(self, parent, id, title)
	self.model = model 
        # Add a panel and some controls to display the size and position
        panel = wx.Panel(self, -1)
        label1 = wx.StaticText(panel, -1, "Old MySql Password(If any):")
        label2 = wx.StaticText(panel, -1, "Desired MySql Password:")
        label3 = wx.StaticText(panel, -1, "Php Version Desired (4/5):")
        self.oldPwdCtrl = wx.TextCtrl(panel, -1, "")
        self.newPwdCtrl = wx.TextCtrl(panel, -1, "")
        self.phpVersionCtrl = wx.TextCtrl(panel, -1, "")
        self.button = wx.Button(panel, -1, "Go Go Lamp!")
        self.panel = panel

        # Use some sizers for layout of the widgets
        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.Add(label1)
        sizer.Add(self.oldPwdCtrl)
        sizer.Add(label2)
        sizer.Add(self.newPwdCtrl)
        sizer.Add(label3)
        sizer.Add(self.phpVersionCtrl)
	sizer.Add(self.button)
	self.button.Bind(wx.EVT_BUTTON, self.OnButton)
	
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizerAndFit(border)
        self.Fit()

    def OnButton(self, evt):
	self.model.set_old_mysql_pwd(self.oldPwdCtrl.GetValue())
	self.model.set_new_mysql_pwd(self.newPwdCtrl.GetValue())
	self.model.set_php_version(self.phpVersionCtrl.GetValue())
	verified = True
	#verify inputs not shit for real
	if verified:
		self.model.SendSuccessMessage()
	else:
	    #update UI
	    return

class WxModel:
	def get_old_mysql_pwd(self):
		print (self.oldPwd)
		return self.oldPwd
	def get_new_mysql_pwd(self):
		return self.newPwd
	def get_php_version(self):
		return self.phpVersion
	def set_old_mysql_pwd(self, val):
		self.oldPwd = val
	def set_new_mysql_pwd(self, val):
		self.newPwd = val
	def set_php_version(self, val):
		self.phpVersion = val	
	def SendSuccessMessage(self):
		self.callBack()	
	def set_callback(self, callBack):
		self.callBack = callBack
##### END WX MODE
 
class Driver: 
	def __init__(self, uiChoice):
		if uiChoice == "c":
			self.model = CLIModel()
			self.app = None
		if uiChoice == "w":
			self.model = WxModel() 
			self.model.set_callback(self.execute)
			self.app = WxLampApp(0,self.model) 
		else:
			exit_route()
			
	def show(self):
		if self.app != None:
			self.app.MainLoop()
		self.execute() 

	def execute(self):
		self.install(self.model.get_php_version(), self.model.get_old_mysql_pwd(), self.model.get_new_mysql_pwd()) 
		self.write_config() 

	def setup_mysql(pwd, oldpwd): 
		db = MySQLdb.connect("localhost","root",oldpwd,"mysql")
		cursor = db.cursor()
		cursor.execute("""UPDATE user SET Password=PASSWORD(%s) WHERE user='root'; FLUSH PRIVILEGES;""", pwd)
	 	
	def install(self, installPhpFive, passwd, oldpwd):
		call("apt-get update")
		if installPhpFive:
			call("apt-get install apache2 php5 libapache2-mod-php5")
		else:
		   	call("apt-get install mysql-server mysql-client php4-mysql")
		setup_mysql(passwd, oldpwd)
		call("apt-get install phpmyadmin")
 
	def write_config(self):
		configFile = open("/etc/apache2/apache2.conf", "a")
		configFile.write("#Include /etc/phpmyadmin/apache.conf")
		configFile.close()

def main(): 
	if len(sys.argv) == 1: 
		exit_route()
	driver = Driver(sys.argv[1].lower())
	driver.show()

main()
