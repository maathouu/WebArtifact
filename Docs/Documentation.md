<h1 style="font-size:3.5rem;">Web Artifact - lightweight multi browser automation</h1> 

<h2 style="font-size:2.5rem;">Basic Infos</h2>

Web Artifact is an open source project which aims to be a Python librairy in the future\
This module provides a portable way to automate interaction with web browsers programmatically\
The structure is designed to be able of managing multi browsers and tab at the same time

---------------------------------- **Source Code** :[Web Artifact](https://github.com/maathouu/WebArtifact) ----------------------------------

> [!WARNING]  
> This project is in early development and isn't fully usable.

---

<h3 style="font-size:2rem;">How to install / import</h3>

For the moment, you can only download the module from [Github](https://github.com/maathouu/WebArtifact/releases/tag/v0.1)

After installing WebArtifact, it may be imported into Python code like:
```python
import WebArtifact as wa
```

<h3 style="font-size:2rem;">Layout</h3>


<h2 style="font-size:2.5rem;">Summuary</h2>



<h2 style="font-size:2.5rem;">Utilisation</h2>



<h2 style="font-size:2.5rem;">Tree Folder</h2>




<h2 style="font-size:2.5rem;">Functioning</h2>

<h3 style="font-size:2rem;">Independants Class</h3>

---

<h4 style="font-size:1.5rem;">ConsoleColor</h4>

`ConsoleColor` is a utility class used throughout the codebase whenever colored output is needed in the python console

It is used in combination with `LogManager.Say` to format log messages with colors and text styles

It does **not contain any functions**, only variables representing ANSI escape codes used for styling terminal output

Each variable (e.g. `CYAN`, `BOLD`, etc.) corresponds to an ANSI escape code

---

<h5 style="font-size:1rem;">Purpose</h5>

- Provide readable aliases for ANSI escape sequences
- Standardize console log formatting
- Enable colored and styled terminal output

---

<h5 style="font-size:1rem;">List of Variables</h5>

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

<h5 style="font-size:1rem;">Example Usage</h5>

```python
LogManager.Say(
    ("Hello in green", ConsoleColor.GREEN),
    "and",
    ("Hello in red", ConsoleColor.RED)
)
```

---

<h5 style="font-size:1rem;">Notes</h5>

> [!NOTE]\
> File: `WebArtifact/Log.py`  
> Created: 0.0.-  
> Last Updated: 0.0.-


---


<h4 style="font-size:1.5rem;">Utility</h4>

`Utility` is a toolbox class with independant helper functions used in mains functions (`GlobalFunction.-` / `FirefoxManager.-`)

Each function includes a minimal documentation (signature,parameters,return type) and <ins>is intended to return a value</ins>.

All `Utility` functions that can fail raise the same exception type (`FlexError`), to allow a better error handling

These functions are pure utilities and **do not directly executes actions on web drivers, browsers, or other external resources**.

---

<h5 style="font-size:1rem;">Purpose</h5>

- Promote code reuse across the project
- Provide the centralization of all helper functions in the same class
- Avoid external extentions whenever possible
- Ensure consistent error handling

---

<h5 style="font-size:1rem;">List of Functions</h5>


<details>
<summary>Decompose</summary>

```python
Text = "   A text  with  a lot of             space at the    start and    the end      "

NewText = Utility.Decompose(Text)
print(NewText)
# >> ["A","text","with","a","lot","of","space","at","the","start","the","and","end"]
```

</details>

---

<details>
<summary>GetFreeRegistredPort</summary>

Section 2

</details>

---

<details>
<summary>GetSocket</summary>

Section 3

</details>

---

<details>
<summary>IsValidApplication</summary>

Section 4

</details>

---

<details>
<summary>ReadIniFile</summary>

Section 5

</details>

---

<details>
<summary>ReadJsonFile</summary>

Section 6

</details>

---

<details>
<summary>SupFLSpace</summary>

Section 7

</details>

---

<details>
<summary>WaitOpenDriver</summary>

Section 8

</details>


---

<h5 style="font-size:1rem;">Notes</h5>

> [!NOTE]\
> File: `WebArtifact/Global.py`  
> Created: 0.0.-\
> Last Updated: 0.1.7

---

<h4 style="font-size:1.5rem;">GlobalFunctions</h4>


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