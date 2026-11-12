import time
import socket
import subprocess
import os
import json
import re

from .Log import ConsoleColor
from .Error import ConfigError,DriverError
from .WebDriver import WebDriver

class Utility:
    def RunCommand(Command:tuple,ErrorClass:object,
                   Shell:bool=False,CaptureOutpout:bool=False,Text:bool=False,Check:bool=False,TimeOut:int=5) -> subprocess.CompletedProcess:
        
        CommandText = " ".join(map(str,Command))
        try:
            return subprocess.run(Command,shell=Shell,capture_output=CaptureOutpout,text=Text,check=Check,timeout=TimeOut)
        
        except FileNotFoundError as E:
            raise ErrorClass(f"Command not found : '{E.filename or CommandText}'",
                             Details={"Command":CommandText,"File":E.filename}) from E
        except PermissionError as E:
            raise ErrorClass(f"Permission denied while running '{CommandText}'",
                             Details={"Command":CommandText,"File":E.filename}) from E
        
        except subprocess.TimeoutExpired as E:
            raise ErrorClass(f"'{CommandText}' did not finish within {TimeOut}s",
                             Details={"Command":CommandText,"TimeOut":TimeOut}) from E
        except subprocess.CalledProcessError as E:
            raise ErrorClass(f"'{CommandText}' failed with exit code {E.returncode}",
                             Details={"Command":CommandText,"ReturnCode":E.returncode,"Stderr":E.stderr}) from E
        
        except OSError as E:
            raise ErrorClass(f"System error while running '{CommandText}' : {E.strerror}",
                             Details={"Command":CommandText,"Errno":E.errno}) from E

    def OpenFile(Path:str,ErrorClass:object,OutPout:str="ReadLines",Encoding:str="utf-8") -> list[str] | dict:
        try:
            with open(Path,"r",encoding=Encoding) as f:
                match OutPout:
                    case "ReadLines":
                        Content = f.readlines()
                    case "Json":
                        Content = json.load(f)
        
        except FileNotFoundError as E:
            raise ErrorClass(f"File not found : '{Path}'",
                             Details={"Path":Path}) from E
        except PermissionError as E:
            raise ErrorClass(f"Permission denied while reading '{Path}'",
                             Details={"Path":Path}) from E
        except json.JSONDecodeError as E:
            raise ErrorClass(f"Invalid JSON in '{Path}' : {E.msg} (line {E.lineno}, column {E.colno})",
                             Details={"Path":Path,"Line":E.lineno,"Column":E.colno}) from E
        
        except OSError as E:
            raise ErrorClass(f"Cannot read '{Path}' : {E.strerror or E}",
                             Details={"Path":Path,"Errno":E.errno}) from E
        except ValueError as E:
            raise ErrorClass(f"Invalid content in '{Path}' : {E}",
                             Details={"Path":Path}) from E
        
        return Content

    def SupFLSpace(Text:str) -> str:
        if len(Text) > 1:
            Index = 0
            while Text[Index] == " " and Index < len(Text):
                Index+=1
            Start = Index
            Index = len(Text)-1
            while Text[Index] == " " and Index != 0:
                Index-=1
            return Text[Start:Index+1]
        else:
            return Text
        
    def IsValidApplication(ApplicationPath:str,ApplicationName:str) -> tuple[bool,str]:
            Result = Utility.RunCommand([ApplicationPath,"--version"],ConfigError,CaptureOutpout=True,Text=True).stdout
            TempLine = Result.splitlines()[0]
            return ApplicationName.lower() in TempLine.lower(),TempLine.lower()
    
    def GetSocket(Port:str) -> str:
        Result = Utility.RunCommand(["netstat","-ano","|","findstr",Port],DriverError,Shell=True,CaptureOutpout=True,Text=True)
        return Result.stdout.split("\n") if Result.returncode == 0 else ""

    def ReadIniFile(FilePath:str) -> dict:
        result = {}
        File = Utility.OpenFile(FilePath,ConfigError)

        ActualSection = None
        for Line in File:
            Line = Utility.SupFLSpace(Line).replace("\n","")
            if len(Line) > 0:
                if Line[0] == "[" and Line[-1] == "]":
                    ActualSection = Line[1:-1]
                    result[ActualSection] = {}
                elif Line[0] != ";":
                    Line = Line.split("=")
                    result[ActualSection][Line[0]] = Line[1]
        return result

    def WaitOpenDriver(Port:str,TimeOut:int) -> int:
        TimeStart = time.time()
        Finished = False
        while time.time() - TimeStart < TimeOut and  not Finished:
            try:
                with socket.create_connection(("localhost", Port),timeout=0.1):
                    return str(time.time() - TimeStart)
            except (ConnectionRefusedError,socket.timeout,OSError):
                time.sleep(0.1)
        raise DriverError(f"Driver on Port {Port} Exceded timeout of {TimeOut}s",
                          Details={"TimeOut":TimeOut,"Port":Port})
        
    def GetFreeRegistredPort(PortRange:tuple,PortForbidden:tuple) -> int:
        PortsCandidates = [Port for Start,End in PortRange for Port in range(Start,End)]
        PortsCandidates = [Port for Port in PortsCandidates if Port not in PortForbidden]

        for Port in PortsCandidates:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('', Port))
                    return str(Port)
                except OSError:
                    continue

        Result = Utility.RunCommand(["netstat","-n"],ConfigError,CaptureOutpout=True,Text=True).stdout

        return list(set(range(49152,65535)) - set([int(x) for x in list(set(re.findall(rb"\b\d+\.\d+.\d+.\d+:(\d+)\b",Result)))]))[0]
        

class GlobalFunction:
    def VerifySocket(LogModule:object,Port:str,ShutDownOtherSession:bool,Driver:str,InstanceName:str) -> None:
        
        LogModule.Say(("Verifying port ",ConsoleColor.BLUE),(Port,ConsoleColor.PURPLE),StartSpace=1)

        Result = Utility.GetSocket(Port)

        if Result != ['']:
            ProcList = []
            
            for Line in Result:
                DecomposedLine = Line.split()
                # DecomposedLine arch : [Protocol , LocalIP , RemoteIP , Status , PID]
                if len(DecomposedLine) > 1:
                    DecomposedLine[-1] = DecomposedLine[-1].replace("\r","").replace("\n","")
                    
                    # Get Executable Path with the PID in Powershell
                    ExecutablePath = Utility.RunCommand(["powershell","-NoProfile","-Command",f"(Get-Process -Id {DecomposedLine[-1]}).Path"],DriverError,CaptureOutpout=True,Text=True).stdout.strip()

                    ProcList.append({"Type":DecomposedLine[0],"LocalAdress":DecomposedLine[1],"DistantAdress":DecomposedLine[2],"Statu":(DecomposedLine[3] if DecomposedLine[0] == "TCP" else ""),"PID":DecomposedLine[-1],"Path":ExecutablePath})
                    LogModule.Say("--> ",(str(ProcList[-1]),ConsoleColor.PURPLE))

                for Line in ProcList:
                    
                    if Line["Type"] == "UDP":
                        raise DriverError(f"Port {Port} have already an active UDP connection",
                                          Details={"Port":Port,"Processus":Line})
                    
                    if Line ["Statu"] == "LISTENING":
                        
                        ApplicationName = os.path.basename(Line["Path"]).lower()
                        if not ApplicationName in (Driver,os.path.splitext(Driver)[0]):
                            raise DriverError(f"'{ApplicationName}' is already listenning on port {Port}",
                                              Details={"Port":Port,"ApplicationName":ApplicationName})

                        # try:
                        #     response = requests.get(f"http://localhost:{Port}/status")
                        #     print(response)
                        # except Exception as E:
                        #     print("jpp wola")
                        
                        # if response.status_code != 200:
                        #     raise InvalidSocket()
                        
                        
                    elif Line["Statu"] in ("ESTABLISHED","CLOSE_WAIT","SYN_SENT","SYN_RECEIVED"):
                        None # ToDO
                    elif Line["Statu"] == "TIME_WAIT":
                        None # ToDo
            else:
                LogModule.Say("==> ",("This socket has no application associated with",ConsoleColor.YELLOW))

    def VerifyUserSettings(LogModule,UserData,Comm,Driver,Browser,InstanceName):
        if Driver == "geckodriver.exe":
            UserData["FirefoxOptions"] = {"args": [],"binary":UserData["BrowserPath"]}
        elif Driver == "":
            ... # ChromiumUpdate

        UsedPort = Comm()["UsedPort"]
        PreUsedPort = Comm()["PreUsedPort"]

        LogModule.Say(("Verifying Applications Path",ConsoleColor.BLUE),StartSpace=1)
        for AppliPath,AppliName in ((UserData["DriverPath"],os.path.splitext(Driver)[0]),(UserData["BrowserPath"],Browser)):
            
            Result = Utility.IsValidApplication(AppliPath,AppliName)

            if Result[0]:
                LogModule.Say("--> ",(Result[1],ConsoleColor.PURPLE))
            else:
                raise ConfigError(f"{Result[1]} isn't a valid application name for {AppliName}",
                                  Details={"ApplicationName":AppliName,"SubprocessResult":Result[1],"SubprocessPath":AppliPath})
        
        LogModule.Say(("Verifying Port Value",ConsoleColor.BLUE),StartSpace=1) 
        if UserData["Port"] != "auto":
            try:
                UserData["Port"] = int(UserData["Port"])
            except (ValueError, TypeError, OverflowError) as E:
                raise ConfigError(f"Invalid Port setting : expected 'auto' or an integer, got {UserData['Port']}",
                                  Details={"Value":UserData["Port"],"ValueType":type(UserData["Port"])})

            if not 1024 < UserData["Port"] < 65536:
                raise ConfigError(f"Port need to be between 1024 and 65536 not included",
                                  Details={"Port":UserData["Port"]})

            if UserData["Port"] in UsedPort:
                raise ConfigError(f"'{UserData['Port']}' is present in used port : {str(UsedPort)}",
                                  Details={"Port":UserData["Port"],"UsedPort":UsedPort})
        else:
            
            Utility.GetFreeRegistredPort(((4434, 4440), (4461, 4479), (4489, 4499), (4504, 4533)),PreUsedPort)

        UserData["Port"] = str(UserData["Port"])
        if UserData["Port"] in PreUsedPort:
            LogModule.Say("==> ",("Port ",ConsoleColor.YELLOW),(UserData["Port"],ConsoleColor.PURPLE),(" is already 'pre' used by another Instance on the module",ConsoleColor.YELLOW))
        else:
            Comm("Add",("PreUsedPort",UserData["Port"]))

        LogModule.Say("--> ",(UserData["Port"],ConsoleColor.PURPLE))

        LogModule.Say(("Verifying Firefox Profil Name",ConsoleColor.BLUE),StartSpace=1)
        if UserData["ProfilName"] == "Temp" and UserData["ProfilPath"] == "":
            LogModule.Say("--> Firefox Profil Name: Temp")
            LogModule.Say("==> ",("A temporary file will be created and deleted automatically",ConsoleColor.YELLOW))
        elif UserData["ProfilName"] != "Temp":
            if Browser == "firefox":
                FirefoxProfilesIniPath = os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox","profiles.ini")
                if not os.path.isfile(FirefoxProfilesIniPath):
                    LogModule.Say("==> ",(FirefoxProfilesIniPath,ConsoleColor.PURPLE),("dosn't exist",ConsoleColor.YELLOW))
                else:

                    Profiles = Utility.ReadIniFile(FirefoxProfilesIniPath)
                    ProfilesInfos = {}
                    for Profile in Profiles:
                        if Profile[:7] == "Profile":
                            LogModule.Say("--> Name : ",(f"{Profiles[Profile]['Name']:<20}",ConsoleColor.PURPLE)," / Path : ",(Profiles[Profile]["Path"],ConsoleColor.PURPLE))
                            ProfilesInfos[Profiles[Profile]["Name"]] = Profiles[Profile]["Path"]
                    if UserData["ProfilName"] in ProfilesInfos:
                        UserData["FirefoxOptions"]["args"] += (["-profile", os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox",ProfilesInfos[UserData["ProfilName"]])])
                        LogModule.Say("==> ",("Firefox Profil Name: ",ConsoleColor.YELLOW),(UserData["ProfilName"],ConsoleColor.PURPLE)," / Profil Path : ",(UserData["FirefoxOptions"]["args"][1],ConsoleColor.PURPLE))
                    else:
                        if UserData["ProfilPath"] != "":
                            LogModule.Say("==> ",("No Profil named : ",ConsoleColor.YELLOW),(UserData["ProfilName"],ConsoleColor.PURPLE))
                        else:
                            raise ConfigError(f"'{UserData['ProfilName']}' isn't present in {FirefoxProfilesIniPath}",
                                              Details={"ProfilName":UserData["ProfilName"],"IniProfil":Profiles,IniProfilPath:FirefoxProfilesIniPath})

            elif Browser == "Chrome":
                ... # ChromiumUpdate
                    
        else:
            LogModule.Say("--> No profil name set")
            LogModule.Say(("Verifying Firefox Profil Path",ConsoleColor.BLUE),StartSpace=1)
            
            TimesFilePath = os.path.join(UserData["ProfilPath"],"times.json")
            TimesFile = Utility.OpenFile(TimesFilePath,ConfigError,OutPout="Json")
            
            if Browser == "firefox":
                FirefoxOptionalFiles = {
                    "prefs.js",         # créé au 1er lancement
                    "places.sqlite",    # Historique et favoris
                    "cookies.sqlite",   # Cookies
                    "cert9.db",         # Certificats 
                    "key4.db"           # Mots de passe 
                }
                TimesFilePath = os.path.join(UserData["ProfilPath"],"times.json")
                
                LogModule.Say("--> ",(f"{'times.json':<20}",ConsoleColor.PURPLE),": ",("present",ConsoleColor.BOLD))
                if ("created","firstUse") != tuple(TimesFile.keys()):
                    raise ConfigError(f"times.json keys : '{tuple(TimesFile.keys())}' isn't equal to '{('created','firstUse')}'",
                                        Details={"TimeKeys":tuple(TimesFile.keys()),"TimeKeysNeeded":tuple(TimesFile.keys())})
                                        
                for OptionalFile in FirefoxOptionalFiles:
                    LogModule.Say("--> ",(f"{OptionalFile:<20}",ConsoleColor.PURPLE),": ",(("present" if os.path.isfile(os.path.join(UserData["ProfilPath"],OptionalFile)) else "absent"),ConsoleColor.BOLD))

                if TimesFile["firstUse"] == None:
                    LogModule.Say("==> ",(f"{TimesFilePath}",ConsoleColor.PURPLE),(" never been luanch before",ConsoleColor.YELLOW))
            
            elif Browser == "chrome":
                ... # ChromiumUpdate

        LogModule.Say(("Finished verifying User settings",ConsoleColor.CYAN),StartSpace=1)
        return UserData