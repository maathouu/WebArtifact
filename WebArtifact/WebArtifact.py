import sys

from .Log import LogManager,ConsoleColor
from .Error import UsageError


class S:
    def __init__(self) -> None:
        
        self.Data = {
            "Instance":{
                "OpenDriverTimeout":5,
                "BrowserOpen":False,
                "ShutDownOtherSession":True,
            },
            "Log":{
                "Save":"both",
                "Mode":"test"
            }
        }
        self.InternalData = {
            "UsedPort":[],
            "PreUsedPort":[],
            "InstanceName":0
        }
        self.Browsers = {

        }
        self.GLog = LogManager(mode=self.Data["Log"]["Mode"],save=self.Data["Log"]["Save"])


    def Firefox(self,GeckodriverPath:str="geckodriver.exe",FirefoxPath:str=r"C:\Program Files\Mozilla Firefox\firefox.exe",ProfilPath:str="",ProfilName:str="Temp",Port="auto",InstanceName:str="$") -> None:
        """
        Create New Firefox Instance and verify user settings.
        
        :param GeckodriverPath: path to geckodriver.exe
        :param FirefoxPath: binary of firefox.exe
        :param ProfilPath: path to any firefox profil
        :param ProfilName: name of a profil in profiles.ini
        :param Port: port to open geckodriver
        :param InstanceName: Instance name
        
        """# :return: somme des deux nombres 
                       
        self.GLog.Changecategory("None")
        if "WebArtifact.Firefox" not in sys.modules:
            from .WebBrowser import FirefoxManager
        else:
            FirefoxManager = sys.modules["WebArtifact.Firefox"].FirefoxManager

        if InstanceName == "$":
            InstanceName = str(self.InternalData["InstanceName"])
            self.InternalData["InstanceName"] += 1
        elif type(InstanceName) != str:
            raise UsageError("Custom instance name isn't an str value",
                             Details={"InstanceName":InstanceName,"InstanceNameType":type(InstanceName)})

        if InstanceName in self.Browsers:
            raise UsageError("Custom instance name specified have already been created",
                             Details={"Instancename":InstanceName,"InstanceNameList":[x for x in self.Browsers]})
            
        self.CurrentWorkingInstance = InstanceName

        self.GLog.Say("Creating a new Firefox Instance : ",(InstanceName,ConsoleColor.PURPLE),StartSpace=1)
        self.GLog.Changecategory("Firefox profil verif")
        self.Browsers[InstanceName] = {
            "Module":FirefoxManager({
                "DriverPath":GeckodriverPath,
                "BrowserPath":FirefoxPath,
                "ProfilPath":ProfilPath,
                "ProfilName":ProfilName,
                "Port":Port,
                "InstanceName":InstanceName
                },
                self.GLog,
                self.Data["Instance"],
                self.Comm),
            "Browser":"Firefox",
            "Statu":0}
        
        self.Browsers[InstanceName]["Statu"] = 1


    def Comm(self,mode="Get",data=None):
        if mode == "Get":
            return self.InternalData
        elif mode == "Set":
            self.InternalData[data[0]] = data[1]
        elif mode == "Add":
            self.InternalData[data[0]].append(data[1])


    def OpenDriver(self,InstanceName="$") -> None:
        
        InstanceName = self._VerifInstanceName(InstanceName,1)
        self.Browsers[InstanceName]["Statu"] = 2

        match self.Browsers[InstanceName]["Browser"]:
            case "Firefox":
                self.GLog.Changecategory("Geckodriver luanch")
                self.Browsers[InstanceName]["Module"].OpenGeckodriver()

            case "Chrome":
                None

        self.Browsers[InstanceName]["Statu"] = 3
            

    def NewSession(self,InstanceName="$") -> None:

        InstanceName = self._VerifInstanceName(InstanceName,3)

        self.Browsers[InstanceName]["Statu"] = 4

        match self.Browsers[InstanceName]["Browser"]:
            case "Firefox":
                self.GLog.Changecategory("Geckodriver New Session")
                self.Browsers[InstanceName]["Module"].NewSession()

            case "Chrome":
                None
    

    def OpenBrowser(self,InstanceName="$"):
        None


    def Luanch(self,InstanceName="$"):
        None






    def _VerifInstanceName(self,InstanceName,MinimumStatu) -> str:
        if not len(self.Browsers) > 0:
            raise UsageError("No instance created")
        
        if InstanceName == "$":
            InstanceName = self.CurrentWorkingInstance
        elif InstanceName not in self.Browsers:
            raise UsageError(f"No instance name '{InstanceName}'",
                             Details={"InstanceName":InstanceName,"InstanceNameList":[x for x in self.Browsers]})
        
        if self.Browsers[InstanceName]["Statu"] < MinimumStatu:
            raise UsageError(f"Instance '{InstanceName}' hasn't a valid statu code",
                             Details={"InstanceName":InstanceName,InstanceStatu:self.Browsers[InstanceName]["Statu"],"MinimumStatu":MinimumStatu})

        return InstanceName