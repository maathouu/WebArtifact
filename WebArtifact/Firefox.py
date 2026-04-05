import os
from .Utility import IsValidApplication,ReadIni

def UserSettingsVer(LogModule,Settings: dict) -> list:
        FirefoxOptions = {
            "args": []
        }
        LogModule.Say("Sarting Verifying User Data")
                                                                                  
        IsValidApplication(LogModule,Settings["DriverPath"],"geckodriver")                                                     # Verifie le path geckodriver
        IsValidApplication(LogModule,Settings["BrowserPath"],"firefox")                                                        # Verifie le path firefox
        FirefoxOptions["binary"] = Settings["BrowserPath"]

        if Settings["ProfilName"] == "Temp" and Settings["ProfilPath"] == "":
            LogModule.Say("Firefox Profil Name: Temp / Profil Path : \n")
        elif Settings["ProfilName"] != "Temp":
            LogModule.Say("Testing Profiles.ini")
            FirefoxProfilesIniPath = os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox","profiles.ini")
            if not os.path.isfile(FirefoxProfilesIniPath):
                LogModule.Say(f"{FirefoxProfilesIniPath} dosn't exist")
            else:
                LogModule.Say(f"Starting analysing {FirefoxProfilesIniPath}")
                Profiles = ReadIni(LogModule,FirefoxProfilesIniPath)
                ProfilesInfos = {}
                for Profile in Profiles:
                    if Profile[:7] == "Profile":
                        LogModule.Say(f"--> Name : {Profiles[Profile]["Name"]:<20} / Path : {Profiles[Profile]["Path"]}")
                        ProfilesInfos[Profiles[Profile]["Name"]] = Profiles[Profile]["Path"]
                if Settings["ProfilName"] in ProfilesInfos:
                    FirefoxOptions["args"] += (["-profile", os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox",ProfilesInfos[Settings["ProfilName"]])])
                    LogModule.Say(f"Firefox Profil Name: {Settings["ProfilName"]} / Profil Path : {FirefoxOptions["args"][1]}")
                else:
                    if Settings["ProfilPath"] != "":
                        LogModule.Say(f"No Profil named {Settings["ProfilName"]}")
                    else:
                        LogModule.SayError(f"No Profil named {Settings["ProfilName"]} found")
        else:
            LogModule.Say(f"Testing {Settings["ProfilPath"]}")
            if os.path.isdir(Settings["ProfilPath"]):
                FirefoxOptionalFile = [
                    "prefs.js",         # créé au 1er lancement
                    "places.sqlite",    # Historique et favoris
                    "cookies.sqlite",   # Cookies
                    "cert9.db",         # Certificats 
                    "key4.db"           # Mots de passe 
                ]








            elif os.path.isfile(Settings["ProfilPath"]):
                LogModule.SayError(f"<< {Settings["ProfilPath"]} >> is a file and not a directory")
            else:
                LogModule.SayError(f"<< {Settings["ProfilPath"]} >> isn't a file or directory")
        return FirefoxOptions

