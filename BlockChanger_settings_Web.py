#from flask import *
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
import hashlib
from netfilterqueue import NetfilterQueue
from responses import Response
from scapy.all import *
import json
import os
from web3 import Web3
import logging
import subprocess
#-----------------------SECRET KEY-------------------------
app = Flask(__name__)
app.secret_key = "M7NK"
app.permanent_session_lifetime = timedelta(days=5)
#------------------------------------------------------------


##############################################################################
##                                 Blockchain Info                          ##
try:
    os.system("clear")
    print("[*] Setting up web3 functions. Please wait...")
    blockchainNetworkIP = "HTTP://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(blockchainNetworkIP))
    jsonArray = '[{"constant":false,"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"Activate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_addr","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_hash_id","type":"string"},{"internalType":"string","name":"_ip","type":"string"},{"internalType":"string","name":"_mac","type":"string"}],"name":"add_device","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"_hash_id","type":"string"}],"name":"authFunc","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"checkAdminIsLoggedIn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"checkIsAdded","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"deActivate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"_Name","type":"string"}],"name":"displayByName","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"enum BlockChanger.State","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"displayInfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"enum BlockChanger.State","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"string","name":"_username","type":"string"},{"internalType":"string","name":"_password","type":"string"}],"name":"loginUser","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"logout","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"string","name":"_username","type":"string"},{"internalType":"string","name":"_password","type":"string"}],"name":"pushAdminInfo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    abi = json.loads(jsonArray)
    contractAddress = "0xCfEB869F69431e42cdB54A4F4f105C19C080A601"
    address = web3.toChecksumAddress(contractAddress)
    contract = web3.eth.contract(address=address, abi=abi)
    web3.eth.defaultAccount = web3.eth.accounts[0] #choose transaction account
    print("[*] web3 is connected!\n---------------------------------------------------------------------------\n")
except:
    print ("Blockchain connection failed")
    logging.error('Blockchain connection failed')
    exit(0)
##                                                                          ##
##############################################################################



@app.route("/")
def home():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        return render_template("index.html")
    else:
        flash("Administrator is not logged in!", "error")
        return redirect(url_for("login"))


@app.route("/login/", methods=["POST","GET"])
def login():
    if (contract.functions.checkIsAdded().call()):
        if (contract.functions.checkAdminIsLoggedIn().call()):
            return redirect(url_for("home"))
        else:
            if request.method == "POST":
                print ("IFFFFFF111")
                #session.pop("")
                username = request.form["username"]
                password = request.form["password"]
                print (username,password)
                if (contract.functions.checkIsAdded().call()):
                    print ("IFFFFF22222")
                    contract.functions.loginUser(web3.eth.defaultAccount, username, password).transact()
                    if (contract.functions.checkAdminIsLoggedIn().call()):
                        print ("IFFF33333")
                        return redirect(url_for("home"))
                    else:
                        flash("Username or password is incorrect!")
                        return redirect(url_for("login"))
                return redirect(url_for("login"))
            else:
                print ("ELSEEEE")
                return render_template("login.html")
    else:
        return redirect(url_for("create_admin"))

@app.route("/create_admin/", methods=["POST","GET"])
def create_admin():
    if (contract.functions.checkIsAdded().call()):
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            contract.functions.pushAdminInfo(web3.eth.defaultAccount,username,password).transact()
            flash("Admin is added!")
        else:
            return render_template("login.html")




# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent = True
#         #user = request.form["user"]
#         #session["user"] = user
#         username = request.form["username"]
#         password = request.form["password"]
#         flash(f"Login sucess, {user}") #POP UP  
#         return redirect(url_for("user"))
#     else:
#         if "user" in session:
#             flash("already logged 7ge")
#             return redirect(url_for("user"))
#         return render_template("login.html")

@app.route("/user") 
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # if "user" in session:
    #     user = session["user"]
    contract.functions.logout().transact()
    flash(f"Administrator is logged out!")
    # session.pop("user", None)
    return redirect(url_for("login"))


# arp scan to get all reserved ips on the network
output = subprocess.getoutput('sudo arp-scan 192.168.1.132 | grep 192 | tail +2') #sudo arp-scan -l | grep 192
arpscan = output.splitlines() 

@app.route("/add_device/", methods =["POST", "GET"])
def detect_device():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "POST":
            print ("IFFF")
            logging.info('Adding device function has been executed!')
            
            print ("arpscan:" , arpscan)
            print (type(arpscan))
            #name = request.form.get("device_name")
            #print ("Name from html: ",name)
            req = request.form
            info = req["arpscan"] # is a parameter from the post request
            name = req["device_name"] # a parameter from the post request
            if name == "":
                flash("You did not enter a name for the device!")
                return render_template("add_device.html",  arpscan=arpscan)
            ip_src = info.split()[0]
            mac_src = info.split()[1]
            print ("Dict from html selection: ", req)
            print ("Device name: ", name)
            print (type(info), " ::" , info)
            print ("IP:", ip_src,type(ip_src))
            print ("MAC:", mac_src,type(mac_src))
            ###########################################################
            deviceCount = contract.functions.getCount().call()
            iplist = ""
            deviceID = ""
            addr = ""
            with open("ip_list.txt","r") as fr:
                iplist = fr.read()
                with open("ip_list.txt","w") as fw:
                    while True:
                        if ip_src not in iplist:
                            if len(iplist) == 0: 
                                iplist = iplist + ip_src 
                            else: 
                                iplist = iplist + "," + ip_src
                            fw.write(iplist)
                            print ("device count:", deviceCount)
                            addr = web3.eth.accounts[deviceCount+1] # return the new address
                            deviceID = hashlib.md5((ip_src + mac_src + "saltValue").encode('utf-8')).hexdigest()# calculate the id
                            tx_hash = contract.functions.add_device(addr, name, deviceID, ip_src, mac_src).transact() # store the id to the blockchain
                            web3.eth.waitForTransactionReceipt(tx_hash)
                            flash( name +" added successfully!\n ID:" + deviceID +"\nYou must reboot the BlockChanger in order to allow new settings to take action")
                            logging.critical(f"{name} added to the blockchain!")
                            #display_by_name(deviceName)
                            return render_template("add_device.html",  arpscan=arpscan)
                        else:
                            flash(f"The device you have added '{name}' is already exists!") 
                            return render_template("add_device.html",  arpscan=arpscan)
            return render_template("add_device.html",  arpscan=arpscan)
        else:
            print ("ELSEEEE")
            return render_template("add_device.html",  arpscan=arpscan)
            
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login"))

# def display_by_name(name):
#     if (contract.functions.checkAdminIsLoggedIn().call()):
#         info = contract.functions.displayByName(name).call()
#         deviceCount = contract.functions.getCount().call()    
#         if info[1] == "":
#             print("\n[*] This device does not exists!\n")
#         else:
#             if info[5] == 0: state = "Active"
#             else: state = "Down"
#             print(f"""Device {deviceCount}:
#             Address: {info[0]}
#             Name: {info[1]}
#             ID: {info[2]}
#             IP: {info[3]}
#             MAC: {info[4]}
#             State: {state}""")
#     else:
#         return redirect(url_for("login"))

@app.route("/displayall", methods=["POST","GET"]) 
def displayAll():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            headings = ("No", "Address", "Device Name", "ID", "IP", "MAC", "Device State")
            print (headings)
            deviceCount = contract.functions.getCount().call()
            #deviceCount = 2
            #accounts = contract.functions.signed_addresses().call() 
            accounts = web3.eth.accounts
            # count = 1
            # info_dict = {}
            # while count < deviceCount:
            #     info = contract.functions.displayInfo(accounts[count]).call()
            #     info_dict[count] =  info
            #     count+=1
            # print(info_dict)
            
            count = 1
            info_array = []
            while count <= deviceCount:
                info = contract.functions.displayInfo(accounts[count]).call()
                info.insert(0,count)
                count +=1
                if info[2] == "":
                    print("\n[*] This device does not exists!\n")
                    break
                else:
                    if info[6] == 0: 
                        state = "Active"
                        info[6] = state
                        info_array.append(info)
                    else: 
                        state = "Down"
                        info[6] = state
                        info_array.append(info)
            print (info_array)
            print(f"Total number of devices: {deviceCount}")
            return render_template("/displayall.html", headings=headings , info_array=info_array)
        else:
            print("ELLSEEE")
            return render_template("/displayall.html")      
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login"))       



@app.route("/activate_device", methods=["POST","GET"])
def activate_device():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "POST":
            print("IIFFFFFF")
            logging.info('Activate device function has been executed!')
            # print("\n[Note] if you do not know the exact name of the meant device, you can get it from display all devices ")
            name = request.form.get("device_name")
            #name = input("Enter device name: ")
            contract.functions.Activate(name).transact()
            info = contract.functions.displayByName(name).call()
            if info[5] == 0 and info[1] != "":
                flash(f"\n[*] {name} is activated!")
                #print (f"\n[*] {name} is activated!")
                logging.critical(f"{name} has been activated!")
                return redirect(request.url)
            else:
                flash(f"device is not activated!\n[*] The device name is not exists or entered wrong!")
                #print("[*] device is not activated!\n[*] The device name is not exists or entered wrong!")
                return redirect(request.url)
        else:
            print("ELSEEEE")
            return render_template("/activate_device.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login")) 


@app.route("/deactivate_device", methods=["POST","GET"])
def deactivate_device():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "POST":
            logging.info('Activate device function has been executed!')
            #print("\n[Note] if you do not know the id of the meant device, you can get it from display all devices")    
            #name = input("Enter device name: ")
            name = request.form.get("device_name")
            tx = contract.functions.deActivate(name).transact()
            print (tx)
            info = contract.functions.displayByName(name).call()
            if info[5] == 1:
                flash(f"{name} is deactivated!")
                #print (f"\n[*] {name} is deactivated!")
                logging.critical(f"{name} has been deactivated!")
                return redirect(request.url)
            else: 
                flash(f"device is not deactivated!\n[*] The device name is not exists or entered wrong!")
                # print("[*] device is not deactivated!\nSomething went wrong!")
                return redirect(request.url)
        else: 
            return render_template("/deactivate_device.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login")) 

@app.route("/reboot", methods=["POST","GET"])
def reboot():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            os.system("sudo reboot")
            return redirect(url_for("home"))
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login")) 

@app.route("/audit", methods=["POST","GET"])
def audit():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            with open("/home/blockchanger/project-files-project-files-ganache/settings.log","r") as f:
                content=f.read()
            return render_template("audit.html", content=content)
        else:
            return render_template("audit.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login")) 

@app.route("/authlog", methods=["POST","GET"])
def authlog():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            with open("/home/blockchanger/project-files-project-files-ganache/audit.log","r") as f:
                content=f.read()
            return render_template("authlog.html", content=content)
        else:
            return render_template("authlog.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login")) 

@app.route("/pihole", methods=["POST","GET"])
def pihole():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            return render_template("pihole.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login"))

@app.route("/homeassis", methods=["POST","GET"])
def homeassis():
    if (contract.functions.checkAdminIsLoggedIn().call()):
        if request.method == "GET":
            return render_template("homeassis.html")
    else:
        flash("Administrator is not logged in!")
        return redirect(url_for("login"))

def _exit():
    os.system("sudo iptables -F")
    print("Exiting...")
    logging.info('Exiting BlockChanger Settings')
    exit(0)

def main():
    choice = ""
    while choice != 6:
        print("\n-----------------------------\n<++ BlockChanger Settings ++>\n-----------------------------")
        print("""
[1] Add new device
[2] Activate device
[3] Deactivate device
[4] Display device information by name
[5] Display all devices information
[6] Exit.""")
        choice = int(input("\n[*] Choose number from the menu to proceed: "))
        if choice == 1:
            detect_device()
        elif choice == 2:
            activate_device()
        elif choice == 3:
            deactivate_device()
        elif choice == 4:
            deviceName = input("enter device name: ")
            display_by_name(deviceName)
        elif choice == 5:
             displayAll()
        elif choice == 6:
            _exit()
        else: print("Wrong entry!")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    logging.basicConfig(level=logging.INFO,filename='settings.log', encoding='utf-8', format='%(asctime)s:%(levelname)s:%(message)s')
    #main()
