### Packages import
import json


### Functions
def read_system_config(path):
    """
    Function reads json_file that describes system and pins
    """
    with open(path, "r") as read_file:
        system_config = json.load(read_file)
    return system_config

def device_pins(device_name, system_config):
    """
    Function reads only required arguments for GPIO object initialization
    Use it like this: object_creation(*device_pins("object", system_config))
    """
    if ("motor" in device_name):
        return (system_config[device_name]['pins']['ENBL'], 
                system_config[device_name]['pins']['M0'],
                system_config[device_name]['pins']['M1'],
                system_config[device_name]['pins']['M2'],
                system_config[device_name]['pins']['DIR'],
                system_config[device_name]['pins']['STEP'],
                system_config[device_name]['zeroDirection'],
                system_config[device_name]['startDirection'],
                system_config[device_name]['startPosition'],
                system_config[device_name]['moveCoeff'],
                device_name)
    elif ("buzzer" in device_name):
        return (system_config[device_name]['pins']['BUZ'], device_name)
    elif ("endpoint" in device_name):
        return (system_config[device_name]['pins']['ENDP'], device_name)
    else:
        print("NO DEVICE!")

def write_system_config(path):
    """
    Mockup function that creates json
    """
    data = {
    "systemType" : "AMC",
    "systemModel" : "Meiji",
    
    "motorX" : {
        "name" : "motorX",
        "model" : "NEMA17",
        "pins" : {
            "ENBL" : 22,
            "M0" : 10,
            "M1" : 9,
            "M2" : 11,
            "DIR" : 27,
            "STEP" : 17,
        },
        "zeroDirection" : False,
        "startDirection" : True,
        "startPosition" : 30000,
        "moveCoeff" : 0.017
    },
    
    "endpointX" : {
        "name" : "endpointX",
        "pins" : {
            "ENDP" : 15,
        }
    },
    
    "motorY" : {
        "name" : "motorY",
        "model" : "NEMA17",
        "pins" : {
            "ENBL" : 22,
            "M0" : 10,
            "M1" : 9,
            "M2" : 11,
            "DIR" : 5,
            "STEP" : 6,
        },
        "zeroDirection" : False,
        "startDirection" : True,
        "startPosition" : 20000,
        "moveCoeff" : 0.017
    },
    
    "endpointY" : {
        "name" : "endpointY",
        "pins" : {
            "ENDP" : 23,
        }
    },
    
    "motorZ" : {
        "name" : "motorZ",
        "model" : "NEMA17",
        "pins" : {
            "ENBL" : 26,
            "M0" : 21,
            "M1" : 20,
            "M2" : 16,
            "DIR" : 13,
            "STEP" : 19,
        },
        "zeroDirection" : False,
        "startDirection" : True,
        "startPosition" : 6300,
        "moveCoeff" : 1
    },
    
    "endpointZ" : {
        "name" : "endpointZ",
        "pins" : {
            "ENDP" : 8,
        }
    },
    
    "buzzer" : {
        "name" : "buzzer",
        "pins" : {
            "BUZ" : 12,
        }
    },
    
    "camera" : {
        "name" : "RPiCamera",
        "camType" : "rpi"
    } 
    }

    with open("system_config.json", "w") as write_file:
        json.dump(data, write_file, indent=4)