import time
import os

import json
import subprocess

class ConsoleColor:
    HEADER = '\033[95m'
    
    CYAN = '\033[96m'                   # Finished function
    GREEN = '\033[92m'                  # Actual category
    RED = '\033[31m'                    # Error
    YELLOW = '\033[33m'                 # Warning / import info
    BLUE = '\033[34m'                   # Starting new function
    PURPLE = '\033[35m'                 # User Settings
    PINK = '\033[38;2;255;105;180m'     # Global Settings
    ORANGE = '\033[38;2;255;165;0m'     # Value calculated by the function ( like time )
 
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LogManager:                                                                                                      
    def __init__(self,mode="normal",save="console"):
        # sys.excepthook = self.CustomError
        self.ErrorData = {
            "Layout":{
                "Firefox": {
                    "VerifProfil": {
                        "ProfilName":{
                            "NoName":"No profil named : '{profil}' found",
                            "Info":"Incorrect profil in profiles.ini"
                        },
                        "times.json": {
                            "InvalidKey":"Invalid times.json content : '{value}'\nValue needed : '{value_needed}'",
                            "Info": "Failed to load times.json"
                        },
                        "ProfilPath":{
                            "IsFile":"Invalid Path : '{path}' is a file and not a directory",
                            "NoFile":"Invalid Path : '{path}' isn't a valid path",
                            "Info":"Failed to find profil directory"
                        },
                        "Info":FirefoxVerifProfil
                    },
                    "OpenDriver":{
                        "Driver":{
                            "Info":"Failed to luanch geckodriver"
                        },
                        "Info":FirefoxDriver
                    }
                },
                "Utility":{
                    "IsValidAppli":{
                        "WrongAppliName":"Incorrect Application name :\nApplication = {Result}\nApplication needed : '{AppliNeeded}'",
                        "Info":"Invalid Application Path/Name"
                    },
                    "IsValidPort":{
                        "InvalidRange":"Invalid port range :\nValue needed = 1024 < Port < 65536\nPort set = {port}",
                        "AlreadyUsed":"Port already used :\nPort Used by this object = {portused}\nPort set = {port}",
                        "Info":"Invalid Port"
                    },
                    "VerifySocket":{
                        "OtherApplication":"Another application is already using this port:\nPort = {port}\nOther application = {data}",
                        "WrongProtocol":"An UDP protocol is already using this port:\nPort = {port}\nOther application = {data}",
                        "UsedSessionPort":"Another session is already using this port:\nPort = {port}\nUsedPort = {usedport}\nSession = {data}\n",                        
                        "NoShutdown":"Another geckodriver proc who's not managed by this object is already using this port:\nPort = {port}\nSession = {data}",
                        "Info":"Invalid Socket"
                    },
                    "WaitOpenDriver":{
                        "TooLong":"{driver} took too long time too luanch : \nTime took= {time}\nTimeout = {timemax}",
                        "Info":"Invalid time to open driver"
                    },
                    "Info":Utility
                },
                "Global":{
                    "Session":{
                        "NoSession":"You need to create a session before",
                        "IncorrectName":"No session named {name} have been created before",
                        "Info":"Failed to find Session"
                    }
                }
            },
            "Public":{
                json.JSONDecodeError:(
                    "Invalid JSON : '{path}'\n{msg}",
                    lambda context , error : context.update({"msg": getattr(error , 'msg', str(error))})
                ),
                FileNotFoundError:(
                    "File not Found :\nPath = {path}",
                    None
                ),
                subprocess.CalledProcessError:(
                    "Command failed :\nPath = {path}\nCode = {returncode}\n Exit = {stdout}\nError = {stderr}",
                    lambda context , error : context.update({"returnedcode":error.returncode,"stderr":error.stderr,"stdout":error.stdout})
                ),
                PermissionError:(
                    "Permission denied :\nPath = {path}\nCode = {errno}\nFile Name = {filename}\nError = {strerror}",
                    lambda context , error : context.update({"filename":error.filename,"strerror":error.strerror,"errno":error.errno})
                ),
                OSError:(
                    "Os Error :\nPath = {path}\nCode = {errno}\nFile Name = {filename}\nError = {strerror}",
                    lambda context , error : context.update({"strerror":error.strerror,"errno":error.errno,"filename":error.filename})
                ),
                ValueError: (
                    "Invalid value :\nValue = {value}\nError = {error}",
                    lambda context , error : context.update({"value": context.get("value"),"error": str(error)})
                ),
                TypeError: (
                    "Invalid type for conversion :\nType = {type}\nError = {error}",
                    lambda context , error : context.update({"type": type(context.get("value")).__name__,"error": str(error)})
                ),
                Exception:(
                    "Unexpected error : {error_type} : {e}",
                    lambda context , error : context.update({"error_type": type(error).__name__ , "e": str(error),})
                ),
            }
        }
        
        self.Save = save
        self.Category = "None"
        self.ErrorCategory = "None"
        
        if self.Save in ("file","both"):
            if not os.path.isdir("Log"):
                os.makedirs("Log")
            if mode == "normal":
                self.File = f"{time.strftime('%Y-%m-%d_%H:%M', time.localtime())}.log"
            elif mode == "test":
                self.File = "Log/Test.log"
            with open(self.File,"w") as TempFile:
                TempFile.write("")

    def Changecategory(self,Com):
        self.Category = Com[0]
        self.ErrorCategory = Com[1]

    def Say(self,*Message,ErrorMessage="",Pp="",Sp="",mode="Normal"):
        Prefix = ("["+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"]",ConsoleColor.BOLD)
            
        if mode == "Normal":
            Prefix = (Prefix," | ",(self.Category,ConsoleColor.GREEN)," | : ")
        elif mode == "Error":
            Prefix = (Prefix," || ",(Pp,ConsoleColor.CYAN)," : ",(Sp,ConsoleColor.CYAN)," ||")
            Message = ()
            for param in ErrorMessage.splitlines():
                Message += ("\n                      ",(param,ConsoleColor.RED))
        elif mode == "Space":
            Prefix = ("\n",Prefix," | ",(self.Category,ConsoleColor.GREEN)," | : ")
            
        if self.Save in ("file","both"):
            RawMessage = ""
            for word in Prefix+Message:
                if type(word) != str:
                    RawMessage += word[0]
                else:
                    RawMessage += word

            with open(self.File, "a") as File:
                File.write(RawMessage+"\n")    

        if self.Save in ("console","both"):
            for word in Prefix+Message:
                if type(word) != str:
                    print(word[1]+word[0]+ConsoleColor.END,end="")
                else:
                    print(word,end="")
            print()

    def SayError(self,error,category,**context):
        if len(category) == 3:
            SecondaryPrefix = self.ErrorData["Layout"][category[0]][category[1]][category[2]]["Info"]
            ExceptionClass = self.ErrorData["Layout"][category[0]][category[1]]["Info"]
        else:
            SecondaryPrefix = self.ErrorData["Layout"][category[0]][category[1]]["Info"]
            ExceptionClass = self.ErrorData["Layout"][category[0]]["Info"]

        if type(error) == str:
            if len(category) == 3:
                config  = self.ErrorData["Layout"][category[0]][category[1]][category[2]][error]
            else:
                config = self.ErrorData["Layout"][category[0]][category[1]][error]
            Message = config.format(**context)
        else:
            config = self.ErrorData["Public"][type(error)]
            if config[1] != None:
                config[1](context,error)
            Message = config[0].format(**context)

        self.Say(ErrorMessage=Message,Pp=self.ErrorCategory,Sp=SecondaryPrefix,mode="Error")
        raise ExceptionClass(self.ErrorCategory,SecondaryPrefix,Message)



class FirefoxVerifProfil(Exception):
    def __init__(self,Pp,Sp,Message):
        pass

class FirefoxDriver(Exception):
    def __init__(self,Pp,Sp,Message):
        pass



class Utility(Exception):
    def __iniy__(self,Pp,Sp,Message):
        pass