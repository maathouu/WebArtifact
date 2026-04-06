# Code Structure

> Use 'From WebArtifact import S'

## ./WebArtifact.py

### Class S (temporary name)

- Basic Info
  - Handles all core functionality of the library.
  - Handles all differents browser and session

- User Functions
  
  - __init__

    - Basic Info
      
      Set self.Data value
      Create self.Browsers to manage session
      Load the Log manager in self.Glog

  - Firefox

    - Basic Info
      
      Create a firefox Session and verify user settings
      
    - functionning

      import '.Firefox' if not already done
      Create a 'SessionName' if user don't specify it
      Init a firefox session in 'self.Browser["Firefox"][SessionName]' with all user settings and the Log manager 

    - Settings
      
      - GeckodriverPath
        
        - default value = "geckodriver.exe"
        - Type Needed = str 
        - Value Needed = port
        - Info : port to open geckodriver on

      - FirefoxPath

        - default value = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        - Type Needed = str
        - Value Needed = Path
        - Info : Path to firefox.exe

      - ProfilPath

        - default value = ""
        - Type Needed = str
        - Value Needed = Path
        - Info : Path to an Firefox profile ( if you set a different ProfilPath and ProfilName ( "Temp" not included ), ProfilName will be selected instead of ProfilPath )

      - ProfilName

        - default value = "Temp"
        - Type Needed = str
        - Value Needed = Name
        - Info : Name of an profile in profiles.ini ( if ProfilName="Temp" : a temporary profil will be created and deleted automatically )

      - port

        - default value = "4445"
        - Type Needed = str / int
        - Value Needed = Path
        - Info : port to open geckodriver on

      - SessionName

        - default value = "$"
        - Type Needed = str
        - Value Needed = any
        - Info : name of the firefox session ( if SessionName="$" SessionName will be named automatically )
          
    - Example

      - Bot = S()
        Bot.Firefox(GeckodriverPath=r"E:\PERSO\Python\Projet\WebArtifact\geckodriver.exe",ProfilName="default")

    - Error

      > 'UserDataVer()' from '.Firefox'
      > 'IsValidApplication()' from '.Utility' by using 'UserSettingsVer()'
      > 'ReadIni() from .Utility by using 'UserSettingsVer()'

- Programm Functions

> No function yet


## ./Log.py

### Class LogManager

- Basic Info
  - Simple log manager
  - can write in console / file or either

- User Functions

  - __init__

    - Basic Info 
    
      Create the session and set the actual mode

    - functioning

      Set self.Save to 'save' 
      Create 'Log' folder in the repertory
      Create a log file if 'self.save' == "console"
      --> 'Log/%Y-%m-%d_%H:%M:%S.log' if 'mode' == "normal"
      --> 'Log/Test.log'

    - Settings

      - mode

        - default value = "normal"
        - Type Needed = "normal" / "test"
        - Value Needed = name
        - Info : Change the log file name ( only work if 'self.save' in ("file","both"))

      - save

        - default value = "console"
        - Type Needed = "console" / "file" / "both"
        - Value Needed = name
        - Info : Change the Output mode according to value
          - create a file and write output in
          - console : write output directly in console
          - both : set the outpout in the file and console
      
    - Example

      - GLog = Log()
      - GLog = Log(mode="test",save="file")

    - Error

      > No error in this function  
  
  - Say

    - Basic Info 
    
      Say message in the selected mode (file / console / both)
      --> You need to create a session to use this function

    - functioning

      output = "'ActualTime' : 'message'\n"
      set outpout in correct save mode selected

    - Settings

      - message
        - default value = ""
        - Type Needed = string
        - Value Needed = sentence
        - Info : sentence who will be displayed
      
    - Example

      - GLog = Log()
        Glog.Say("Log manager launched")

    - Error

      > No error in this function

  - SayError

    - Basic Info 
    
      Say message in the selected mode (file / console / both) and stop the programm
      --> You need to create a session to use this function

    - functioning

      output = "'ActualTime' : ≠≠> 'message'\n"
      set outpout in correct save mode selected, then raise an error
      ( Use LogManager.Say("≠≠> "+ErrorMessage) )

    - Settings

      - message
        - default value = ""
        - Type Needed = string
        - Value Needed = sentence
        - Info : sentence who will be displayed
      
    - Example

      - GLog = Log()
      - Glog.SayError("Log manager launched")

    - Error

      > No error in this function

- Programm Functions
  -

## ./Utility.py

### No class

- Basic Info
  - toolbox for mains programm functions
  - lot of independants functions are here

- User Functions
  -

- Programm Functions

  - Decompose

    - Basic Info

      split string variable by space into a list

    - functioning

      delete all space in 'Text' and place each word in 'Result'
      return 'Result'

    - Settings 

      - Text
        - default value = 
        - Type Needed = string
        - Value Needed = sentence/word
        - Info : Data who will be split

    - Example 
      - print(Decompose("  Hello    im a  new programmer  "))
        --> ["Hello","im","a","new,"programmer"]
    
    - Error

      > No error in this function

  - SupFLSpace

    - Basic Info

      delete all firsts and lasts spaces in a sentence/word

    - functioning

      delete all space before the first chractere and all space after the last charactere

    - Settings 

      - Text
        - default value = 
        - Type Needed = string
        - Value Needed = sentence/word
        - Info : Data who will -

    - Example 
      - print(SupFLSpace("  Hello    im a  new programmer  "))
        --> "Hello    im a  new programmer"
    
    - Error

      > No error in this function

  - IsValidApplication

    - Basic Info

      Check if a path is the real application asked for

    - functioning

      - Check if the file exist
      - Check if Application name is in the first line of ['ApplicationPath',"--version"] (no cass restriction)

    - Settings 

      - LogModule
        - default value = 
        - Type Needed = Module
        - Value Needed = Log Manager
        - Info : Actual log manager

      - ApplicationPath
        - default value = 
        - Type Needed = string
        - Value Needed = Path
        - Info : Path of the application to check

      - ApplicationName
        - default value = 
        - Type Needed = string
        - Value Needed = Application name ( without extention)
        - Info : Official application name

    - Example 
      - IsValidApplication(self.GLog,"geckodriver.exe","geckodriver")

    - Error

      - "'ApplicationPath' isn't a valid Path" if isn't a valid
      - "'TempLine' isn't 'ApplicationName'" if 'ApplicationName' not in ['ApplicationPath',"--version"]
      - "Unexpected Error : 'SubprocessResult.stderr'\n≠≠>'SubprocessResult.stdout'" if subprocess returncode != 0

  - ReadIni

    - Basic Info

      Read an Ini File and transform its content into dict value

    - functioning

      - Check each line one by one
      - if first and last charactere of a line is [] a new key is added with the section name
      - elif the first charactere isn't ;, the line is splited by = and stored in the dict

    - Settings 

      - LogModule
        - default value = 
        - Type Needed = Module
        - Value Needed = Log Manager
        - Info : Actual log manager

      - FilePath
        - default value = 
        - Type Needed = string
        - Value Needed = Path
        - Info : Path of the Ini file to get

    - Example 
      - print(ReadIni(self.GLog,"C:\Windows\system.ini"))
        --> {"386Enh":{"woafont":"dosapp.fon","EGA80WOA.FON":"EGA80WOA.FON","EGA40WOA.FON":"EGA40WOA.FON","CGA80WOA.FON":"CGA80WOA.FON","CGA40WOA.FON":"CGA40WOA.FON"},"drivers":{"wave":"mmdrv.dll","timer":"timer.drv"},"mci":{}}

    - Error

      - "'ApplicationPath' isn't a valid Path" if isn't a valid
      - "'TempLine' isn't 'ApplicationName'" if 'ApplicationName' not in ['ApplicationPath',"--version"]
      - "Unexpected Error : 'SubprocessResult.stderr'\n≠≠>'SubprocessResult.stdout'" if subprocess returncode != 0

## ./Firefox.py

### class FirefoxManager

