from .Common import *

class CantOpenDriver(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Driver:str,
                ParentModule:str,
                Line:int,
                Port:str,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                
                **Param
                ) -> None:
        """
        Param: 
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