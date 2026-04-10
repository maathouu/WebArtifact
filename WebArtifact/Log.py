import time
import os

import json
import subprocess

class LogManager:                                                                                                      
    def __init__(self,mode="normal",save="console"):                                                                                # save="console" : retranscrit dans la console / save="file" : retranscrit dans un fichier
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
                    }
                },
                "Utility":{
                    "IsValidAppli":{
                        "WrongAppliName":"Incorrect Application name : '{Result}'\nApplication needed : '{AppliNeeded}'",
                        "Info":"Invalid Application Path/Name"
                    },
                    "IsValidPort":{
                        "InvalidRange":"Invalid port range :\nValue needed = 1024 < Port < 65536\nValue got = {port}",
                        "Info":"Invalid Port"
                    },
                    "Info":Utility
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
                    "Invalid integer value :\nValue = {value}\nError = {error}",
                    lambda context , error : context.update({"value": context.get("value"),"error": str(error)})
                ),
                TypeError: (
                    "Invalid type for int conversion :\nType = {type}\nError = {error}",
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
        if self.Save=="file":
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
        self.Errorcategory = Com[1]


    def Say(self,Message="",ErrorMessage="",Pp="",Sp="",mode="Normal"):
        Prefix = "["+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"]"                                                           # Affiche la date et l'heure de chaque action
            
        if mode == "Normal":
            Prefix += " | "+self.Category+" | : "
        elif mode == "Error":
            Prefix += " || "+Pp+" : "+Sp+" ||"
            for param in ErrorMessage.splitlines():
                Message += "\n                      "+param
        else:
            Prefix = "\n"+Prefix+" | "+self.Category+" | : "
            
        if self.Save == "file":
            with open(self.File, "a") as File:
                File.write(Prefix+Message+"\n")
        else:
            print(Prefix+Message)


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

        self.Say(ErrorMessage=Message,Pp=self.Errorcategory,Sp=SecondaryPrefix,mode="Error")
        raise ExceptionClass(self.Errorcategory,SecondaryPrefix,Message)



class FirefoxVerifProfil(Exception):
    def __init__(self,Pp,Sp,Message):
        pass

class Utility(Exception):
    def __iniy__(self,Pp,Sp,Message):
        pass