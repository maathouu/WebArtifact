# Code Structure

> Use 'From WebArtifact import *'

## ./WebArtifact.py


### Class S (temporary name)


- Basic Info
  - Handles all core functionality of the library.
  - This class will be renamed and better distributed in future versions.

- User Functions

  - __init__

    - Basic Info

      Create the session and load variable

    - functioning
      
      Create principal Variable 
        - $UserData (store users settings in)
        - $Data
        - $FirefoxOptions
      
      Initailise log manager with $GLog
      Verify user settings with ~VerInit()

    - Settings
      
      - GeckodriverPath
        - ="geckodriver.exe"
        - Path to geckodriver.exe

      - FirefoxPath 
        - =r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        - Path to firefox.exe

      - ProfilPath
        - ="$Temp"
        - Firefox profils path or "$Temp" to use a temporary file ( managed by geckodriver )
    
      - port
        - ="4445"
        - Loopback port used by geckodriver

    - Example

      - Bot = S()
      - Bot = S(ProfilPath=r"C:\\Users\\-\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\-.default-release")

    - Error

      > No error in this function

  - OpenDriver

    - Basic Info

        Open the Driver ( geckodriver )
        --> You need to create a session to use this function

    - functioning

      Verify selected port with ~VerifySocket()
      launch geckodriver with '$self.UserData[GeckoDriverPath] --port self.UserData[Port]' on $ Driver
      Wait till driver is launched with ~WaitOpenDriver

    - Settings 
      
      > No settings in this function

    - Example

      - Bot = S()
        Bot.OpenDriver()

    - Error
      
      > No error in this function


  - OpenBrowser

    - Basic Info

      Open the Browser ( firefox )
      --> You need to create a session and open the driver to use this function

    - functioning
      
      Send launching request with ~RequestPost http://localhost:$UserData[Port]/session , {"capabilities": {"alwaysMatch": {"browserName": "firefox","moz:firefoxOptions":$FirefoxOptions}}}
      Set $Data[SessionID] with response of request
      Turn $Data[BrowserOpen] to True
      
    - Settings

      > No settings in this function

    - Example 
      - Bot = S()
        Bot.OpenDriver()
        Bot.OpenBrowser()
    
    - Error
      
      > No error in this function

  - CloseDriver
  
    - Basic Info

      Close the Driver ( geckodriver ) and Browser ( firefox )
      --> You need to create a session and open the driver to use this function


    - functioning

      Close Browser if opened with ~CloseBrowser
      Send stop request to driver
      Wait till it stop

    - Settings 

      > No settings in this function
    
    - Example 
      - Bot = S()
        Bot.OpenDriver()
        Bot.OpenBrowser()
        Bot.CloseDriver()

      - Bot = S()
        Bot.OpenDriver()
        Bot.CloseDriver()

    - Error

      > No error in this function

  - KillDriver
  
    - Basic Info

      Kill the Driver ( geckodriver ) and Browser ( firefox )
      --> You need to create a session and open the driver to use this function

    - functioning

      Close Browser if opened with ~CloseBrowser
      Kill proc

    - Settings 

      > No settings in this function
    
    - Example 
      - Bot = S()
        Bot.OpenDriver()
        Bot.OpenBrowser()
        Bot.KillDriver()

      - Bot = S()
        Bot.OpenDriver()
        Bot.KillDriver()

    - Error

      > No error in this function

  - KillDriver
  
    - Basic Info

      close the browser
      --> You need to create a session / open the driver and open the browser to use this function

    - functioning

      send delete request with $Data[SessionID]
      set Data[BrowserOpen] to False

    - Settings 

      > No settings in this function
    
    - Example 
      - Bot = S()
        Bot.OpenDriver()
        Bot.OpenBrowser()
        Bot.CloseBrowser()

    - Error

      > No error in this function


- Programm Functions

  - VerInit

    - functioning
      
      Verify Some $UserData settings one by one
        - Geckodriver path with ~IsValidApplication
        - Firefox path with ~IsValidApplication
          Add firefox path in $FirefoxOptions
        - ProfilPath
          if $Temp -> Nothing
          else -> verify with '$UserData[FirefoxPath] -profile $UserData[ProfilPath] -headless -no-remote' and add profil path to $FirefoxOptions

    - Settings

      > No settings in this function

    - Error
      
      - 'Profile cannot be used by Firefox' if profil path isn't valid

  - VerifySocket

    - functioning
      
      Extract socket info with 'netstat -ano | findstr : self.UserData[Port]'
      Verify if port is used by another application with 'taskkill /PID €PID /F'
      Shut down last Geckodriver proc if already launched

    - Settings

      > No settings in this function

    - Error
      
      - 'Another application is already using this port (Name)' if an application is already using the port on TCP and isn't geckodriver
      - 'Another application is already using this port (Protocol)' if an UDP protocol is already using the port
      - '--> Unexpected Error : €SubprocessResult.stderr \n ≠≠> €SubprocessResult.stdout' Unexpected Error (surely if the programm can't kill the last geckodriver proc)

  - WaitOpenDriver

    - functioning
      
      Try to create a connection with driver port each 0.1 seconds
      return time taken

    - Settings 

      > No settings in this function

    - Error
      
      - 'GeckoDriver took too long time to launch : $Data[OpenDriverTimeout] s' if time taken > $Data[OpenDriverTimeout]

  - RequestPost

    - functioning
      
      post request with given link and data
      return response

    - Settings 

      - link
        - loopback driver link

      - data
        - format : json

    - Error
      
      - 'Session Response havn t a valid statu_code : €TempSessionResponse.status_code \n≠≠> €TempSessionResponse.text' if request code != 200

  - IsValidApplication

    - functioning
      
      Verify if path to the application exist
      Extract version of the application with '€ApplicationPath --version'
      Verify if the application name is in the €SubprocessResult

    - Settings 

      - ApplicationPath
        - path to the application (given by the user)

      - data
        - application name (given by the programme)

    - Error
      
      - '--> << €ApplicationPath >> isn't a valid Path' if application path isn't valid
      - '--> Unexpected Error : €SubprocessResult.stderr \n≠≠> €SubprocessResult.stdout' Unexpected Error
      - '--> TempLine isn't << €ApplicationName >>' if given application path isn't the the asked application
      - '--> << €ApplicationPath >> isn't a valid €ApplicationName  Version/Apllication' if given application path isn't a valid application at all


### Class Log


- Basic Info
  - Simple log manager
  - can write in console / file or either

- User Functions

  - __init__

    - Basic Info 
    
      - Create the session and set the actual mode

    - functioning

      Set $Save to €save 
      Create 'Log' folder in the repertory
      Create a log file if €save = 'console'
      --> 'Log/%Y-%m-%d_%H:%M:%S.log' if mode = 'normal'
      --> 'Log/Test.log'

    - Settings

      - mode
        - ='normal'
        - can be 'normal' or 'test' : change the log file name

      - save
        - ='console'
        - can be 'console' / 'file' / 'both' : change outpout mode
          - file : create a file and write output in
          - console : write output directly in console
          - both : set the outpout in the file and console
      
    - Example

      - GLog = Log()
      - GLog = Log(mode="test",save="file")

    - Error

      > No error in this function

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