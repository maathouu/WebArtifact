import time
import os

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
        self.Category = Com

    def Say(self,*Message,mode="Normal"):
        if mode != "Blank":
            Prefix = ("["+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"]",ConsoleColor.BOLD)
            if mode == "Normal":
                Prefix = (Prefix," | ",(self.Category,ConsoleColor.GREEN)," | : ")
            elif mode == "Space":
                Prefix = ("\n",Prefix," | ",(self.Category,ConsoleColor.GREEN)," | : ")
        else:
            Prefix = ()
            
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

    def SayError(self,Var):
        ErrorData = {key:value for key,value in vars(Var).items()}
        self.Say((">> ERROR",ConsoleColor.RED),mode="Blank")
        self.Say(("==> Context :",ConsoleColor.RED),mode="Blank")
        for DisplayElement in ("GlobalContext","Context","DetailedContext"):
            self.Say(("--> "+DisplayElement+" : "+ErrorData[DisplayElement],ConsoleColor.RED),mode="Blank")
            del ErrorData[DisplayElement]
        self.Say(("==> Param :",ConsoleColor.RED),mode="Blank")
        for DisplayElement in ErrorData:
            self.Say(("--> "+DisplayElement+" : "+str(ErrorData[DisplayElement]),ConsoleColor.RED),mode="Blank")