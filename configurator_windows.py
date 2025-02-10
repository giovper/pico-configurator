# LO SCOPO DI QUESTO FILE E' QUELLO DI PERMETTERE DI PERSONALIZARE L'INSTALLAZIONE SUL PICO (CON CIRCUIT PYTHONO MICRO PYTHON
# E CONFIGURARE IL FILE PAYLOAD.DD E I DATI RELATIVI

#!\usr\bin\env\python3

#Import libraries

import os

from time import sleep 

def is_raspberry_pi(letter):
    try:
        file = open(f"{letter}:\INFO_UF2.TXT", "r")
        file.close()
        return True
    except FileNotFoundError:
        return letter.upper()[0] >= "D" and letter.upper()[0] <= "Z" and letter.upper()[2:] == "-force" #force

def does_device_exists(letter):
    return os.path.exists(f"{letter}:\\")

def get_uf2_file(name):
    if name == "Circuit Python":
        return "circuit_python.uf2"
    elif name == "Micro Python":
        return "micropython.uf2"
    else:
        print("Error: UF2 file not found. Now using Circuit Python; please check the var uf2_name")
        return "circuit_python.uf2"
    
uf2_name = "Circuit Python"

#Welcome

print("Welcome to the raspberry configurator script, please choose a program: \n")

#Get the required instructions

print("1) Default\t 2) Ducky Rickroll")

print("3) Ducky Hacked Message\t 4) Custom\n")

programNum = 0

while programNum > 4 or programNum < 1: 
    try:
        programNum = int(input("Please type a number and press enter: "))
    except ValueError:
        pass

print(f"Selected {programNum}\n")

#Preparing the pico

input("Please hold the boot select button and connect the pico. Press enter when it shows up...")

sleep(1)

#Get drive letter

letter = input("Please enter the device letter: ")

while not is_raspberry_pi(letter):
    print(f"Device <{letter}> doesn't seem to be a raspberry pi pico. You can use # -force but only do if you're sure it's a RP Pico and you plugged it in pressing the BOOTSEL button " if does_device_exists(letter) else f"Device <{letter}> not found")
    letter = input("Please enter the device letter: ")

print(f"Letter <{letter}> good")

sleep(1)

print("Formating pico...")

os.system(f"copy src\\format.uf2 {letter}:\ ")

sleep(6)

print("Flashing circuit python...")        

os.system(f"copy src\{get_uf2_file(uf2_name)} {letter}:\ ")

sleep(6)

print("Copying libraries...")

os.system(f"mkdir {letter}:\lib\\adafruit_hid ")
os.system(f"copy src\lib\\adafruit_hid {letter}:\lib\\adafruit_hid\ ")


print("LIBRARIES COPIED")

sleep(2)

print("Copying main program...")

os.system(f"copy src\code.py {letter}:\code.py")

sleep(2)

print("Preparation done!\n")

#Flashing the right program

config = ["info: Raspberry Pi Pico configurated"]

if programNum == 1:
    config.append(f"runConfig: default")

elif programNum == 2:
    os.system(f"copy src\scripts\\rickrollsimple.dd {letter}:\payload.dd")
    config.append(f"runConfig: ducky")

elif programNum == 3:
    os.system(f"copy src\scripts\hacked.dd {letter}:\payload.dd")
    config.append(f"runConfig: ducky")

elif programNum == 4:
    config.append(f"runConfig: custom")


open(f"{letter}:\config.ini", "x")
configFile = open(f"{letter}:\config.ini", "w")
configFile.write("\n".join(config))
configFile.close()

print(f"Program {programNum} flashed\n")
print("Your pico is ready to go but please do not use this for mailicious purposes... :)")

sleep(0.5)

exit("Bye!")
