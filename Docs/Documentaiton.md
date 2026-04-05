# Code Structure

> Use 'From WebArtifact import S'

## ./WebArtifact.py

### Class S (temporary name)

- Basic Info
  - Handles all core functionality of the library.
  - This class will be renamed and better distributed in future versions.

- User Functions
  
  - Firefox

    - Basic Info
      
      - Select the browser to firefox and driver to geckodriver
      - Set main settings for the browser and driver
      
    - functionning

      - import Firefox.py to get needed functions
      - Set User settings function in 'self.UniversalUserData'
      - Set main settings in 'self.UniversalData'
      - Load log manager from '.Log' as self.GLog
      - Verifying User settings function with 'UserSettingsVer()' from '.Firefox'
        'UserSettingsVer()' return result in 'self.FirefoxOptions'

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

    - Example

      - Bot = S()
      - Bot.Firefox(GeckodriverPath=r"E:\PERSO\Python\Projet\WebArtifact\geckodriver.exe",ProfilName="default")

    - Error

      > 'UserSettingsVer()' from '.Firefox'
      > 'IsValidApplication()' from '.Utility' by using 'UserSettingsVer()'

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
    
      - Create the session and set the actual mode

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

  ===================
  
  
  - Say

    - Basic Info 
    
      - Say message in the selected mode (file / console / both)
      --> You need to create a session to use this function

    - functioning

      output '€ActualTime : €message\n' in the file / console

    - Settings

      - message
        - string message to say
      
    - Example

      - GLog = Log()
      - Glog.Say("Log manager launched")

    - Error

      > No error in this function

  - SayError

    - Basic Info 
    
      - Say message in the selected mode (file / console / both) and stop the programm
      --> You need to create a session to use this function

    - functioning

      output '€ActualTime : €message\n' in the file / console
      raise and Error with the same message

    - Settings

      - message
        - string message to say
      
    - Example

      - GLog = Log()
      - Glog.SayError("Log manager launched")

    - Error

      > No error in this function

- Programm Functions
  -


### Other


- Decompose

  - Basic Info

    split string vcariable by space into a list

  - functioning

    delete all space in €Text and place each word in €Result
    return €Result

  - Settings 

    - Text
      - string variable 

  - Example 
    - r = Decompose("  Hello    im a  new programmer  ")
      --> ["Hello","im","a","new,"programmer"]
  
  - Error

    > No error in this function


# To do