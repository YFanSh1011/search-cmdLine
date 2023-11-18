## Introduction

"search" is a selenium-based command line tool that helps users search for information using designated or predefined browsers and search engines. It simplifies the process of automated web searches by providing a convenient command line interface.

## Prerequisites

Before you install and use "search", you need to ensure the following prerequisites are met:

1. **Browser Installation**:
- "search" requires either Google Chrome or Mozilla Firefox to be installed on your system. 
- You can verify this by checking the version of your browser.

2. **Correct Version of WebDriver**:
- Depending on your browser, ensure you have the corresponding WebDriver installed:
  - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) for Google Chrome.
  - [GeckoDriver](https://github.com/mozilla/geckodriver) for Mozilla Firefox.
- You can verify the WebDriver installation by checking its version in the command line.

    - For ChromeDriver:
        ```
        chromedriver --version
        ```

    - For GeckoDriver:
        ```
        geckodriver --version
        ```

Make sure that the versions of the browser and the WebDriver are compatible. Refer to the respective WebDriver documentation for compatibility details.



## Installation

To install this tool, you'll need Python installed on your system. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

Once Python is installed, you can install this tool directly from the source. Here are the steps:

1. **Clone the Repository (optional):**
   If you have `git` installed, you can clone the repository directly. Otherwise, you can download the source code as a zip file from [GitHub](https://github.com/YFanSh1011/search-cmdLine.git).
  
2. **Build the Package:**
This command compiles the package and prepares it for installation.
    ```
    python setup.py build
    ```

3. **Install the Package:**
This will install the package into your Python environment.
    ```
    python setup.py install
    ```

After completing these steps, your tool should be installed and ready to use. You can verify the installation by running 
```
search --help
```

# Usage


## Flags

## Default

## Search Engine Settings

# Examples
