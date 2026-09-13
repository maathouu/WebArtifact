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

---


<h3 style="font-size:2rem;">Version System</h3>

<h4 style="font-size:1.5rem;">Working</h4>

WebArtifact use a common managing system used on all my project\
It's a **3 digit versioning system** following the format **`Major.Minor.Patch`** : 

- The **first digit** (`Major`) represents the **Global Category** of the project. It defines the project's main guidelines and architecture. Changes to this number are **extremely rare**
- The **second digit** (`Minor`) represents the **Global Subcategory**. It is incremented when a **major feature or update** has been completed and groups together all previous `Patch` versions into a stable release
- The **third digit** (`Patch`) represents a **Micro Version**. It is used for all `Minor` changes such as new small features, function improvements, bug fixes, or documentation updates

`Patch` versions do **not** have a dedicated roadmap. Every Patch change is documented in the **Versions** folder\

---

<h4 style="font-size:1.5rem;">Version Agreement</h4>

Each `Patch` file follows a set of rules that can evolve over time. The current **Version Agreement** is `0.0`\
The first line of every file states the Version Agreement used for that file (*ex: Agreement Version : 0.0*)

<details>
<summary>Version 0.0</summary>

- The file is organized using **tags** in the format `==== ==== ] $ [ ==== ====`\
  There are **3 types of tags**: `Main Change` / `Little Change` / `Commit`

- Each modification has a **title** and a **description**\
  The title is composed of **3 parts**:
  
  - **Modification action**: a restricted keyword ( ex: `Created` / `Deleted` / `Append` / `Modified` / `Reworked` / `Fixed` / `Updated` )
  - **Modification type**: the type of file/section affected by the change ( ex: `Documentation` / `Function` / `Variable` / `Advertisement` / `Raise` )
  - **Modification section**: the location of the change, written as a path with `>` for classes/functions/variables/titles ( ex: `/WebArtifact/Global.py > Utility > Decompose()` )

  The description have no rule

</details>


<!-- <h4 style="font-size:1.5rem;">Version Agreement</h4>

Each `Patch` file are governed by established rules that can change over the time. The current Version Agreement is 0.0\
The first line in every file is the Version Agreement used on the file (*ex : Agreement Version : 0.0*)

<details>
<summary>Version 0.0</summary>

- Files is organised with balise '==== ==== ] $ [ ==== ===='\
  There're 3 type of Balise : Main Change / Little Change / Commit
- Each modification have a title and a description\
  Title is composed of 3 parts : 
  - modification change : Restricted word (ex : Created / Deleted / Append / Modified / Reworked / Fixed / Updated )
  - modification type : It's the type of file / section who have been modifified / deleted ... (ex : Documentation / function / variable / Advertissment / raise)
  - modification section : It's where the modification have been : composed with a path and '>' for class / function | for title in the doc file | for variable  (ex : /WebArtifact/Global.py > Utility > Decompose() ) 


</details> -->



---




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
<summary>GetFreeRegistredPort</summary>

---

### Description

This function **search and valid** an available network port in a defined range *(by avoiding forbidden port)*\
If no port is available in the specified range, the function will scan every availible port directly with the systeme

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`PortRange`** | `tuple[tuple[int, int], ...]` | `((4434, 4440), (4461, 4479))` | Port range list to test. Each sub-tuple contains `(StartPort, EndPort)` |
| **`PortForbidden`** | `tuple[int, ...]` | `(4444, 4445)` | List of port already used by the module |
| **`return`** | `int` | `4434` | Available port found |

---

### Functioning & Usage

The function generate a list of candidate ports by combining all `PortRange` range and by excluding port in `PortForbidden`

1. **Active Strategie :** Function try linking sequentially (*bind*) to each candidates ports by using `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. **BackUp Strategie :** If no port is available, function will extract the result of `netstat -n` to identify and return the first free port

---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |
| **`InvalidUserSetting`** | **Yes** | `Subprocess` | Handle subprocess for `netstat -n` |


---

> [!NOTE]\
> Created: 0.1.1  
> Last Updated: 0.1.1

</details>

---

<details>
<summary>GetSocket</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`Port`** | `int` | `4444` | Port to verify |
| **`return`** | `str` | #TD | Result of the port analyse |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-

</details>

---

<details>
<summary>IsValidApplication</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`return`** |  |  |  |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-

</details>

---

<details>
<summary>ReadIniFile</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`return`** |  |  |  |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-

</details>

---

<details>
<summary>ReadJsonFile</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`return`** |  |  |  |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-v

</details>

---

<details>
<summary>SupFLSpace</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`return`** |  |  |  |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-

</details>

---

<details>
<summary>WaitOpenDriver</summary>

---

### Description

---

### Parametres & return

| Parametre | Type | Exemple | Description |
| :--- | :--- | :--- | :--- |
| **`return`** |  |  |  |

---

### Functioning & Usage



---

### Error manager

| Type | FlexError | Unexpected | Description |
| :--- | :--- | :--- | :--- |



---

> [!NOTE]\
> Created: 0.-.-
> Last Updated: 0.-.-

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