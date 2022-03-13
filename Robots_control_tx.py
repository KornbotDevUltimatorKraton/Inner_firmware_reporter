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
camera_list = subprocess.check_output("v4l2-ctl --list-devices",shell=True) 
serial_count = []
cam_list_mem = {}
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

     for camin in count(0):

           print("Processing loop 2 ",camin) 
          
#Client receive the message from the speech recogintion software running deeply processing 
def Speech_recognition(): 
     pass 
     

def mainbody_status_devices():
      Camera_list_devices()        
      for ty in count(0):
            host_info = host_info_callback(path_serial)
            dict_host_info = {'PID_process':os.getpid(),host_namea.hostname:ipa.ip,'Serial_devices':host_info,'I2C devices address':i2c.scan(),'Camera_list':cam_list_mem}
            print(dict_host_info)
            jsondata = json.dumps(dict_host_info) 
            message = pickle.dumps(jsondata) 
            sock1.sendto(message,(address,5080))        
              
#Core processing multithreading status of the function reading from multithread
if __name__ =="__main__":

             #These loop will working on the threading programmable add function by exec  
             p1 = multiprocessing.Process(target=mainbody_status_devices)
             p2 = multiprocessing.Process(target=Camera_streaming)
             p1.start()
             p2.start()
             p1.join()
             p2.join()
      
