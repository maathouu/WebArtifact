<h1 style="font-size:3rem;">Web Artifact - lightweight multi browser automation</h1> 

<h2 style="font-size:2rem;">Basic Infos</h2>

Web Artifact is an open source project which aims to be a Python librairy in the future\
This module provides a portable way to automate interaction with web browsers programmatically\
The structure is designed to be able of managing multi browsers and tab at the same time

---------------------------------- **Source Code** :[Web Artifact](https://github.com/maathouu/WebArtifact) ----------------------------------

> [!WARNING]  
> This project is in early development and isn't fully usable.

<h3 style="font-size:1.5rem;">How to install / import</h3>

For the moment, you can only download the module from [Github](https://github.com/maathouu/WebArtifact/releases/tag/v0.1)

After installing WebArtifact, it may be imported into Python code like:
```python
import WebArtifact as wa
```

<h3 style="font-size:1.5rem;">Layout</h3>


<h2 style="font-size:2rem;">Summuary</h2>



## Utilisation



## Tree Folder




<h2 style="font-size:2rem;">Functioning</h2>

### Independants Class


#### ConsoleColor

`ConsoleColor` is a utility class used throughout the codebase whenever colored output is needed in the python console

It is mainly used in combination with `LogManager.Say` to format log messages with colors and text styles

It does **not contain any functions**, only variables representing ANSI escape codes used for styling terminal output

Each variable (e.g. `CYAN`, `BOLD`, etc.) corresponds to an ANSI escape code

---

##### Purpose

- Provide readable aliases for ANSI escape sequences
- Standardize console log formatting
- Enable colored and styled terminal output

---

##### List of Variables

```python
HEADER = '\033[95m'

# Color
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'

PINK = '\033[38;2;255;105;180m'
ORANGE = '\033[38;2;255;165;0m'

# Styles
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
```

---

##### Example Usage

```python
LogManager.Say(
    ("Hello in green", ConsoleColor.GREEN),
    "and",
    ("Hello in red", ConsoleColor.RED)
)
```

---

##### Notes

> [!NOTE]
> File: `WebArtifact/Log.py`  
> Created: 0.0.-  
> Last Updated: 0.0.-


#### Utility





#### GlobalFunctions


### Object Class


#### S

#### LogManager

#### FirefoxManager


### Errors Class


#### InvalidSocket

#### InvalidUserSettings

#### UnexpectedError


<!-- > [!NOTE]  
> Highlights information that users should take into account, even when skimming.

> [!TIP]
> Optional information to help a user be more successful.

> [!IMPORTANT]  
> Crucial information necessary for users to succeed.

> [!WARNING]  
> Critical content demanding immediate user attention due to potential risks.

> [!CAUTION]
> Negative potential consequences of an action.

<span style="color:green">Added in version 0.0.2<br>Changed in version 0.1.0</span> -->