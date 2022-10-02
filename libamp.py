#!/usr/bin/python3

# Send RC5-encoded commands.
# Confirmed working with:
#   Cambridge Audio azur 540A v2

import pigpio

pi = pigpio.pi()


#############
# CONSTANTS #
#############

RC5_PER = 889 # half-bit period (microseconds)
#CA_RC5_SYS = 16

devs = {
    'CXA80': 16, 
    'CXC': 20,
    '640T': 17,
    'CXA60': 16
}

cmds = {
    'CXA80': {
 'Power_Toggle': 12,
'Power_On': 14,
'Power_Off': 15,
'Mute_Toggle': 13,
'Mute_On': 50,
'Mute_Off': 51,
'Volume_Up': 16,
'Volume_Down': 17,
'LCD_Bright': 18,
'Brightness_Toggle': 72,
'LCD_Dim': 19,
'LCD_Off': 71,
'Speaker_Select': 20,
'Speaker_AB': 30,
'Speaker_A': 35,
'Speaker_B': 39,
'Analogue_Stereo_Direct': 78,
'Trigger_A': 82,
'Trigger_B': 83,
'Trigger_C': 84,
'Source_Up': 99,
'Source_Down': 126,
'A1': 100,
'A2': 101,
'A3': 102,
'A4': 103,
'A1_(Balanced)': 104,
'D1': 105,
'D2': 106,
'D3': 107,
'MP3_': 108,
'USB_Audio': 114,
'Bluetooth': 115
    },
        'CXA60': {
 'Power_Toggle': 12,
'Power_On': 14,
'Power_Off': 15,
'Mute_Toggle': 13,
'Mute_On': 50,
'Mute_Off': 51,
'Volume_Up': 16,
'Volume_Down': 17,
'LCD_Bright': 18,
'Brightness_Toggle': 72,
'LCD_Dim': 19,
'LCD_Off': 71,
'Speaker_Select': 20,
'Speaker_AB': 30,
'Speaker_A': 35,
'Speaker_B': 39,
'Analogue_Stereo_Direct': 78,
'Trigger_A': 82,
'Trigger_B': 83,
'Trigger_C': 84,
'Source_Up': 99,
'Source_Down': 126,
'A1': 100,
'A2': 101,
'A3': 102,
'A4': 103,
'D1': 105,
'D2': 106,
'D3': 107,
'MP3_': 108,
'USB_Audio': 114
    },
    'CXC': {
        '0': 0,
'1': 1,
'2': 2,
'3': 3,
'4': 4,
'5': 5,
'6': 6,
'7': 7,
'8': 8,
'9': 9,
'Power_Toggle': 12,
'Power_On': 50,
'Power_Off': 51,
'-/--_10+': 14,
'LCD_Bright': 18,
'LCD_Dim': 19,
'LCD_Off': 71,
'Brightness_Toggle': 72,
'Info': 21,
'Play/Pause': 24,
'Play': 53,
'Pause': 48,
'Random': 28,
'Repeat': 29,
'Skip_right': 32,
'Skip_left': 33,
'Prog': 36,
'>>': 43,
'<<': 44,
'Eject': 45,
'Menu': 52,
'Stop': 54,
'Remain': 61,
'Select/Enter': 87
    },
    '640T': {
        'Power': 124,
'Brightness': 71,
'Auto_Tune': 117,
'Mute': 116,
'Preset_1': 91,
'Preset_2': 92,
'Preset_3': 93,
'Preset_4': 94,
'Preset_5': 95,
'Preset_6': 96,
'Preset_7': 97,
'Preset_8': 98,
'Preset_9': 99,
'Preset_10': 100,
'Scroll_Up': 77,
'Scroll_Down': 78,
'Select': 87,
'Info': 121,
'FM/DAB': 101,
'Alarm': 125
    }
}
# dictionary of possible commands, mapped to the code we need to send
cmd = {
        'aux': 4,
        'cd': 5,
        'tuner': 3,
        'dvd': 1,
        'av': 2,
        'tapemon': 0,
        'vol-': 17,
        'vol+': 16,
        'volup': 17,
        'voldown': 16,
        'mute': 13,
        'standby': 12,
        'bright': 18,
        'source+': 19,
        'source-': 20,
        'sourcenext': 19,
        'sourceprev': 20,
        'clipoff': 21,
        'clipon': 22,
        'muteon': 50,
        'muteoff': 51,
        'ampon': 14,
        'ampoff': 15
        }

#############
# Functions #
#############
global toggle
toggle = False # How to make persistent???

def help(dev):
    for com in cmds[dev]:
        print(com) 


# build RC5 message, return as int
def build_rc5(dev,cmd):
    # TBD: check whether dev / cmd exist....

    global toggle
    RC5_CMD = int(cmds[dev][cmd])
    RC5_START = 0b100 + (0b010 * (RC5_CMD<64)) + (0b001 * toggle)
    RC5_SYS = int(devs[dev])

    # RC-5 message has a 3-bit start sequence, a 5-bit system ID, and a 6-bit command.
    RC5_MSG = ((RC5_START & 0b111) << 11) | ((RC5_SYS & 0b11111) << 6) | (RC5_CMD & 0b111111)
    toggle = not toggle
    return RC5_MSG

# manchester encode waveform. Period is the half-bit period in microseconds.
def wave_mnch(DATA, PIN):
    pi.set_mode(PIN, pigpio.OUTPUT) # set GPIO pin to output.

    # create msg
    # syntax: pigpio.pulse(gpio_on, gpio_off, delay us)
    msg = []
    for i in bin(DATA)[2:]: # this is a terrible way to iterate over bits... but it works.
        if i=='1':
            msg.append(pigpio.pulse(0,1<<PIN,RC5_PER)) # L
            msg.append(pigpio.pulse(1<<PIN,0,RC5_PER)) # H
        else:
            msg.append(pigpio.pulse(1<<PIN,0,RC5_PER)) # H
            msg.append(pigpio.pulse(0,1<<PIN,RC5_PER)) # L

    msg.append(pigpio.pulse(0,1<<PIN,RC5_PER)) # return line to idle condition.
    pi.wave_add_generic(msg)
    wid = pi.wave_create()
    return wid

# manchester encode waveform. Period is the half-bit period in microseconds.
def print_mnch(DATA):
    
    # create msg
    # syntax: pigpio.pulse(gpio_on, gpio_off, delay us)
    msg = []
    for i in bin(DATA)[2:]: # this is a terrible way to iterate over bits... but it works.
        if i=='1':
            msg.append(0) # L
            msg.append(1) # H
        else:
            msg.append(1) # H
            msg.append(0) # L
    for m in msg:
        print(m)
    print("")
    return msg

# check for positive integer
def posint(n):
    try:
        if int(n)>0:
            return int(n)
        else:
            raise ValueError
    except ValueError:
            msg = str(n) + " is not a positive integer"
            raise argparse.ArgumentTypeError(msg)

def execute(pin, device, command, repeat):

    for i in range(repeat):
	# generate RC5 message (int)
    	rc5_msg = build_rc5(device, command)

    	# generate digital manchester-encoded waveform
    	wid = wave_mnch(rc5_msg, pin)

    #for i in range(repeat):
        cbs = pi.wave_send_once(wid)

def print_(msg):
    print("{0:b}".format(msg))
