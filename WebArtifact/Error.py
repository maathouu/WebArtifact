import json
import subprocess


# ========================================= [ Error ToolBox ] =========================================


class FlexError(Exception):
    def __init__(self,**kwargs):
        for Key,Value in kwargs.items():
            setattr(self,Key,Value)

class UnexpectedError:
    def InvalidFile(ErrorModule,File):
        if isinstance(ErrorModule,FileNotFoundError):
            Context = f"Invalid Path : '{File}' -> Path dosn't exist"
        elif isinstance(ErrorModule,PermissionError):
            Context = f"Invalid Path : '{File}' -> Invalid Permission"
        elif isinstance(ErrorModule,OSError):
            Context = f"Invalid Path : '{File}' -> ..."
        elif isinstance(ErrorModule,json.JSONDecodeError):
            Context = f"Invalid File Content : '{File}' -> Can't convert file content into dict"
            DetailedContext = ErrorModule.msg

        if isinstance(ErrorModule,(FileNotFoundError,PermissionError,OSError)):
            DetailedContext = ErrorModule.strerror

        return Context,DetailedContext

    def InvalidSubprocess(ErrorModule,command): # TM
        if isinstance(ErrorModule,subprocess.CalledProcessError): # if Check = True
            Context = ""
            DetailedContext = ErrorModule.stderr
        elif isinstance(ErrorModule,PermissionError):
            Context = f"Invalid permission to execute the command : {command}"
        elif isinstance(ErrorModule,OSError):
            Context = ""
        elif isinstance(ErrorModule,FileNotFoundError):
            Context = f"Invalid Path in command : {command}"
        
        if isinstance(ErrorModule,(FileNotFoundError,PermissionError,OSError)):
            DetailedContext = ErrorModule.strerror
        
        return Context,DetailedContext


# ========================================= [ Global Error] =========================================


class InvalidSocket(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                InstanceName:str,
                Driver:str,
                Port:str,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param
                ) -> None:
        """
        Param: commands / Process ID / UsedPort / Processus Information
        """
        self.GlobalContext = f"Error while analysing port {Port} for {InstanceName}"
        if Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext

        self.InstanceName = InstanceName
        self.Driver = Driver
        self.Port = int(Port)

        self.ErrorModule = ErrorModule
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)

class InvalidUserSettings(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                InstanceName:str,
                Driver:str,
                
                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param) -> None:
        """
        Param: ApplicationNeeded / ApplicationGot / ApplicationPath / Port / UsedPort / ProfilName / IniProfil / IniProfilPath / TimeKeys / TimeKeysNeeded
        """
        self.GlobalContext = f"Error while analysing user settings for Insatnce {InstanceName}"
        if Unexpected == "File":
            self.Context,self.DetailedContext = UnexpectedError.InvalidFile(ErrorModule,Param["File"])
        elif Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext

        self.InstanceName = InstanceName
        self.Driver = Driver

        self.ErrorModule = ErrorModule
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)


# ========================================= [ WebArtifact Error] =========================================


class BadUtilisation(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                
                DetailedContext:str=None,
                **Param) -> None:
        """
        Param: InstanceNameGot / InstanceNameUsed / FunctionUsed
        """
        self.GlobalContext = f"Error with direct use of commands"
        self.Context = Context
        self.DetailedContext = DetailedContext

        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)


# ========================================= [ WebDriver Error] =========================================


class CantOpenDriver(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                InstanceName:str,
                Driver:str,
                Port:str,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                
                **Param
                ) -> None:
        """
        Param: 
        """
        self.GlobalContext = f"Error while attempting to open {Driver} for Instance {InstanceName}"
        if Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext

        self.InstanceName = InstanceName
        self.Driver = Driver
        self.Port = int(Port)

        self.ErrorModule = ErrorModule
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)

class DriverConnection(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                InstanceName:str,
                Driver:str,
                Port:str,
                Method:str,
                Route:str,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                
                **Param
                ) -> None:
        """
        Param: 
        """
        self.GlobalContext = f""
        

        self.InstanceName = InstanceName
        self.Driver = Driver
        self.Port = int(Port)
        self.Method = Method
        self.Route = Route

        self.ErrorModule = ErrorModule
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)