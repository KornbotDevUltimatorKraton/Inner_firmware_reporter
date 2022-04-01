import cv2, imutils,socket,os,pickle,json,re,subprocess # Getting the main python data  and data streaming from the list 
import sys 
import pandas as pd 
import subprocess
from itertools import count
from sys import platform 
import requests # Getting the requests from the server to get the gpio data for the configuretion gpio   
import numpy as np
import time
import base64
import multiprocessing
import threading # Getting the multithreading 
import board
import busio
import getpass
import math 
user = getpass.getuser() 
i2c = busio.I2C(board.SCL, board.SDA)
host_OEM = subprocess.check_output("uname -a",shell=True).decode().split(" ")[2]
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
server_socket.connect(("8.8.8.8", 80))
host_name = socket.gethostname()
host_ip = server_socket.getsockname()[0]
print(host_name,host_ip) # Getting the local ip address of the robot 
path_serial = "/sys/class/tty"
try:
   camera_list = subprocess.check_output("v4l2-ctl --list-devices",shell=True) 
except: 
   print("No camera attach")
serial_count = []
cam_list_mem = {}
audio_mem = []
PATHUDP = "/home/"+user+"/UDP_camera_streaming_realtime_video/" # UDP camera input from this path of the directory 
PATH_SR = "/home/"+user+"/Bot_listener/"    # PATH_

class Robotbody: #Object oriented programming 
    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip

print(Robotbody(host_name,host_ip))
host_namea = Robotbody(host_name,host_ip)
print("Get host name ",host_namea.hostname)
ipa = Robotbody(host_name,host_ip)
print("Get Local IP addresses ",ipa.ip)
os_list = ['windows','win32','linux']
print("plat form",platform,sys.platform.startswith (platform))
print("Sensor address scanner ",i2c.scan()) # Getting the number of the i2c address 
print(host_OEM)
sock1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #getting the remote socket 
address = "192.168.50.201"  #Get this ip from the sdcard reader code uploader 
#Local communication between the function 
sock_local = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
address_local = ("127.0.0.1",5080)
sock_local.bind(address_local)  
def host_info_callback(path_serial):
       
       list_serial = os.listdir(path_serial)
       for l in range(0,len(list_serial)):
          
           if len(list_serial[l].split("ttyACM")) >1: 
              
              if list_serial[l] not in serial_count: 
                  serial_count.append(list_serial[l])      
           if len(list_serial[l].split("ttyUSB")) >1: 
               if list_serial[l] not in serial_count:
                     serial_count.append(list_serial[l])
       for check_serial in serial_count: 
                       if check_serial not in list_serial: 
                                      serial_count.remove(check_serial) #remove the list of the serial in case not found attach on physical devices connection 
                               
       #dict_host_info = {host_namea.hostname:ipa.ip,'Serial_devices':serial_count}
       return serial_count        
def Camera_list_devices(): 
   try:
      print(camera_list.decode().split("\n\t"))
      cam_devices = camera_list.decode().split("\n\t")                  
      for r in range(5,len(cam_devices)):
               if len(cam_devices[r].split("/dev/video")) == 2:
                      if cam_devices[r].split("/dev/video")[1].isdigit() == False: 
                            print(cam_devices[r].split("/dev/video")[1])
                            if r+1 <= len(cam_devices):
                                  cam_list_mem[cam_devices[r].split("/dev/video")[1].split("\n\n")[1].split(":")[0]] = cam_devices[r+1].split("/dev/video")[1]
   except: 
        print("No camera devices attached")
def Camera_image_processing():      
     for camin in count(0):
           print("Processing loop 1 ",camin)
          
def Camera_streaming(): 
     Run_udpcam = subprocess.check_output("python3 "+PATHUDP+"UDPserver.py",shell=True)
     print(Run_udpcam)
     for camin in count(0):
              data,addr = sock_local.recvfrom(1024)
              received  = pickle.loads(data)
              message = json.loads(received)
              print(message,type(message),addr) # Getting the data of the udp camera error to reset the default mode
              

def List_audio_devices(): 
            check_audio_devices = subprocess.check_output("aplay -l",shell=True)
            list_audio = check_audio_devices.decode().split("\n") #Getting the list audio devcies 
            for r in range(1,len(list_audio)): 
                       if  len(list_audio[r].split(' Subdevice ')) == 1 and len(list_audio[r].split("  Subdevices:")) !=2:
                                                    print(list_audio[r].split(" Subdevice "),type(list_audio[r].split(" Subdevice ")))
                                                    if list_audio[r].split(" Subdevice ") not in audio_mem and list_audio[r].split(" Subdevice ") != ['']:   
                                                       audio_mem.append(list_audio[r].split(" Subdevice "))
#Client receive the message from the speech recogintion software running deeply processing 
def Speech_recognition(): 
        run_bot_listen = subprocess.check_output("python3 "+PATH_SR+"listening.py",shell=True) 
        
#Getting the distance from the RSSI algorithm 
def distance_RSSI(Pt,Pl,rssi): 
      A = Pt-Pl 
      c_dat = (A-rssi)*0.014336239
      d = math.pow(10,c_dat) 
      return d 
def rssi_distance_converter(): 
     bssid_list = subprocess.check_output("iwlist scanning",shell=True)
     data_raw_decode = bssid_list.decode() # decode the raw data 
     #Finding the Signal strange from the list index
     for i in data_raw_decode.split(":"): 
         try:

           if len(i.split("=")) == 3:
                    
                     rssi = int(i.split("=")[2].split("\n")[0].split(" ")[0]) 
                     Pl = int(i.split("=")[1].split(" ")[0].split("/")[0]) 
                     Pt = int(i.split("=")[1].split(" ")[0].split("/")[1])
                     distance = distance_RSSI(Pt,Pl,rssi)
                     print("Output distance ",Pt,Pl,rssi," dbm",distance-2.55," m") 
                     return distance-2.55   
         except: 
             pass 
 
def RSSI_data(): 
     bssid_list = subprocess.check_output("iwlist scanning",shell=True)
     data_raw_decode = bssid_list.decode() # decode the raw data 
     #Finding the Signal strange from the list index
     for i in data_raw_decode.split(":"): 
         try:
           
           if len(i.split("=")) == 3:
                     print(i.split("=")[2].split("\n")[0]) 
                     return i.split("=")[2].split("\n")[0].split(" ")[0]
          
         except: 
              pass
def Scanning_nearby_signal(): 
     bssid_list = subprocess.check_output("sudo iwlist scanning",shell=True)
     data_raw_decode = bssid_list.decode() # decode the raw data 
     #Finding the Signal strange from the list index
     for i in data_raw_decode.split(":"): 
         try:

           if len(i.split("=")) == 3:
                     print(i.split("=")[2].split("\n")[0]) 
                     return i.split("=")[2].split("\n")[0].split(" ")[0]

         except: 
              pass


def Cosine_cal_XY(d1,d2,d3): #Getting 3 sources of the
         
        posd = ((math.pow(d1,2)-math.pow(d2,2))-math.pow(d3,2))/(2*d1*d2)
        angletheta = math.acos(posd) # Need to convert to degree 
        degreeangle = math.degrees(angletheta)         
        return degree_angle  # Getting the degree angle 

def polar_angle(d_input,degree_data): #Getting the X,Y coordinate from the list of wifi data input          
        x = d_input*math.cos(degree_data) # Getting the input degree data to calculate x axis 
        y = d_input*math.sin(degree_data)   
        return x,y

# Getting the publisher and subscriber to running in multiple messaging local ip and local machine 
def publish_subscriber(logic,num,input_message,address,port):
          #Subscriber 
          if logic == False:
                
                exec("socket_"+str(num)+" = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
                exec("address = "+"("+str(address)+","+str(port)+")") # Getting the port 
                exec("sock_"+str(num)+".bind("+str(address)+")") 
                exec("data_"+str(num)+",addr_"+str(num) + " = sock_"+str(num)+".recvfrom(4096)") 
                exec("received_"+str(num) +" = pickle.loads(data)") 
                exec("message_"+str(num)  +"= json.loads(received_"+str(num)+")")  
          
          #Publisher           
          if logic == True: 
                exec("socket_"+str(num)+" = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
                exec("address_"+str(num)+" = "+"("+str(address)+","+str(port)+")") # Getting the port 
                #checking the type of the input data
                list_type = ['dict','str']
                check_messagetype = str(type(input_message)).split(" ")[1].split(">")[0]
                if  check_messagetype == list_type[0]: # Dict type 
                          exec("jsondata_"+str(num)+" = json.dumps("+input_message+")") 
                          exec("message_"+str(num)+" = pickle.dumps(jsondata_"+str(num)+")") 
                          exec("sock_"+str(num)+".sendto(message_"+str(num)+",(address_"+str(num)+str(address)+","+str(port)+")") 
                          
                if check_messagetype == list_type[1]: # String type         
                          exec("message_"+str(num)+" = str("+input_message+").encode()") 
                          exec("sock_"+str(num)+".sendto(message_"+str(num)+",(address_"+str(num)+str(address)+","+str(port)+")")

def CPU_temperature(): 
                temp_raw = subprocess.check_output("vcgencmd measure_temp",shell=True)
                temp_dec = temp_raw.decode()
                print(temp_dec)
                return temp_dec.split("\n")[0]
def Bot_listener_Data(): 
       Speech_recognition()

def mainbody_status_devices(): 
      for ty in count(0):
            Camera_list_devices()
            List_audio_devices()
            rssi_raw = RSSI_data()
            cpu_temp = CPU_temperature()
            rssi_distance = rssi_distance_converter() 
            host_info = host_info_callback(path_serial)
            dict_host_info = {'PID_process':os.getpid(),host_namea.hostname:ipa.ip,'Serial_devices':host_info,'I2C devices address':i2c.scan(),'Camera_list':cam_list_mem,'Audio_list':audio_mem,'RSSI':rssi_raw,'RSSI_distance':rssi_distance,'CPU_temp':cpu_temp}
            print(dict_host_info)
            jsondata = json.dumps(dict_host_info) 
            message = pickle.dumps(jsondata) 
            sock1.sendto(message,(address,5080))        
              
#Core processing multithreading status of the function reading from multithread
if __name__ =="__main__":

             #These loop will working on the threading programmable add function by exec  
             p1 = multiprocessing.Process(target=mainbody_status_devices)
             p2 = multiprocessing.Process(target=Camera_streaming)
             p3 = multiprocessing.Process(target=Bot_listener_Data)
             p1.start()
             p2.start()
             p3.start()
             p1.join()
             p2.join()
             p3.join() 
      
