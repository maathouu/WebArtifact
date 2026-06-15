from .Common import *

class InvalidSocket(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Port:str,
                Driver:str,
                ParentModule:str,
                Line:int,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param
                ) -> None:
        """
        Param: commands / Process ID / UsedPort / Processus Information
        """
        self.GlobalContext = f"Error while analysing port {Port} for {Driver} in {ParentModule}"
        if Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext

        self.ErrorModule = ErrorModule
        self.Port = int(Port)
        self.Line = Line
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)

class InvalidUserSettings(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Driver:str,
                ParentModule:str,
                Line:int,
                
                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param) -> None:
        """
        Param: ApplicationNeeded / ApplicationGot / ApplicationPath / Port / UsedPort / ProfilName / IniProfil / IniProfilPath / TimeKeys / TimeKeysNeeded
        """
        self.GlobalContext = f"Error while analysing user settings for {Driver} in {ParentModule}"
        if Unexpected == "File":
            self.Context,self.DetailedContext = UnexpectedError.InvalidFile(ErrorModule,Param["File"])
        elif Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext
        self.ErrorModule = ErrorModule
        self.Line = Line
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)

class BadUtilisation(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Line:int,
                
                DetailedContext:str=None,
                **Param) -> None:
        """
        Param: SessionNameGot / SessionNameUsed
        """
        self.GlobalContext = f"Error with direct use of commands"
        self.Context = Context
        self.DetailedContext = DetailedContext

        self.Line = Line
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)