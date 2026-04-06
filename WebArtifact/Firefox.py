import os
import json
from .Utility import IsValidApplication,ReadIni

class FirefoxManager:

    def __init__(self,UserData:dict,LogModule) -> None:
        self.UserData = UserData
        self.LogModule = LogModule
        self.UserDataVer()

    def UserDataVer(self):
            self.UserData["FirefoxOptions"] = {"args": []}
            self.LogModule.Say("Sarting Verifying User Data")
                                                                                    
            IsValidApplication(self.LogModule,self.UserData["DriverPath"],"geckodriver")                                                     # Verifie le path geckodriver
            IsValidApplication(self.LogModule,self.UserData["BrowserPath"],"firefox")                                                        # Verifie le path firefox
            self.UserData["FirefoxOptions"]["binary"] = self.UserData["BrowserPath"]

            if self.UserData["ProfilName"] == "Temp" and self.UserData["ProfilPath"] == "":
                self.LogModule.Say("Firefox Profil Name: Temp / Profil Path : \n")
            elif self.UserData["ProfilName"] != "Temp":
                self.LogModule.Say("Testing Profiles.ini")
                FirefoxProfilesIniPath = os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox","profiles.ini")
                if not os.path.isfile(FirefoxProfilesIniPath):
                    self.LogModule.Say(f"{FirefoxProfilesIniPath} dosn't exist")
                else:
                    self.LogModule.Say(f"Starting analysing {FirefoxProfilesIniPath}")
                    Profiles = ReadIni(self.LogModule,FirefoxProfilesIniPath)
                    ProfilesInfos = {}
                    for Profile in Profiles:
                        if Profile[:7] == "Profile":
                            self.LogModule.Say(f"--> Name : {Profiles[Profile]["Name"]:<20} / Path : {Profiles[Profile]["Path"]}")
                            ProfilesInfos[Profiles[Profile]["Name"]] = Profiles[Profile]["Path"]
                    if self.UserData["ProfilName"] in ProfilesInfos:
                        self.UserData["FirefoxOptions"]["args"] += (["-profile", os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox",ProfilesInfos[self.UserData["ProfilName"]])])
                        self.LogModule.Say(f"Firefox Profil Name: {self.UserData["ProfilName"]} / Profil Path : {self.UserData["FirefoxOptions"]["args"][1]}")
                    else:
                        if self.UserData["ProfilPath"] != "":
                            self.LogModule.Say(f"No Profil named {self.UserData["ProfilName"]}")
                        else:
                            self.LogModule.SayError(f"No Profil named {self.UserData["ProfilName"]} found")
            if len(self.UserData["FirefoxOptions"]["args"]) == 0:
                self.LogModule.Say(f"Testing manualy {self.UserData["ProfilPath"]}")
                if os.path.isdir(self.UserData["ProfilPath"]):
                    FirefoxOptionalFiles = {
                        "prefs.js",         # créé au 1er lancement
                        "places.sqlite",    # Historique et favoris
                        "cookies.sqlite",   # Cookies
                        "cert9.db",         # Certificats 
                        "key4.db"           # Mots de passe 
                    }
                    TimesFilePath = os.path.join(self.UserData["ProfilPath"],"times.json")
                    try:
                        with open(TimesFilePath,"r") as File:
                            TimesFile = json.load(File)
                    except FileNotFoundError:
                        self.LogModule.SayError(f"| Incorrect Firefox Profil | File not Found : '{TimesFilePath}'")
                    except PermissionError:
                        self.LogModule.SayError(f"| Incorrect Firefox Profil | Permision denied: '{TimesFilePath}'")
                    except json.JSONDecodeError as E:
                        self.LogModule.SayError(f"| Incorrect Firefox Profil | Invalid JSON : '{TimesFilePath}'\n{E.msg}")
                    except Exception as E:
                        self.LogModule.SayError(f"| Incorrect Firefox Profil | Unexpected error : {type(E).__name__} : {E}")
                    
                    self.LogModule.Say(f"--> {"times.json":<20}: present")
                    if ("created","firstUse") != tuple(TimesFile.keys()):
                        self.LogModule.SayError("")

                    for OptionalFIle in FirefoxOptionalFiles:
                        self.LogModule.Say(f"--> {OptionalFIle:<20}: {"present" if os.path.isfile(os.path.join(self.UserData["ProfilPath"],OptionalFIle)) else "absent"}")

                    if TimesFile["firstUse"] == None:
                        self.LogModule.Say(f"==> '{TimesFilePath}' never been luanch before")

                elif os.path.isfile(self.UserData["ProfilPath"]):
                    self.LogModule.SayError(f"<< {self.UserData["ProfilPath"]} >> is a file and not a directory")
                else:
                    self.LogModule.SayError(f"<< {self.UserData["ProfilPath"]} >> isn't a file or directory")

