## Introduction

"search" is a command line tool that helps users search for information using designated or predefined browsers and search engines. It simplifies the process of automated web searches by providing a convenient command line interface.

## Prerequisites

Before you install and use "search", you need to ensure the following prerequisites are met:

**Browser Installation**:
- "search" requires either Google Chrome or Mozilla Firefox to be installed on your system. 
- You can verify this by checking the version of your browser.


## Installation

To install this tool, you'll need Python installed on your system. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

Once Python is installed, you can install this tool directly from the source. Here are the steps:

### Clone the Repository:
   If you have `git` installed, you can clone the repository directly. Otherwise, you can download the source code as a zip file from [GitHub](https://github.com/YFanSh1011/search-cmdLine.git).
  

### Creating an Alias for the 'search' Command

#### For Unix-based Systems:

In the same shell profile file (`~/.bashrc` or `~/.zshrc`):

1. Add the following alias (replace `/path/to/directory` with your directory path):
    ```
    alias search='python /path/to/directory/main.py'
    ```
2. Save the file and exit the editor.
3. Apply the changes with `source ~/.bashrc` (or `source ~/.zshrc` for Zsh).


### Verification
After completing these steps, your tool should be installed and ready to use. You can verify the installation by running: 
```
search --help
```

# Usage
To perform basic web-based search from your terminal, simple use the following syntax:
```
search [keyword] -o [browser] -s [search engine]
```
This command will launch the search engine in the browser as you have specified, and search for web-based content using the keyword provided.


## Flags
The entire functionalities are listed as follows:
```
usage: main.py [-h] [-s SEARCH_ENGINE] [-b BROWSER] [-t TYPE] [-a]
[--change-default] [--display-default] [--show-functions] keyword

positional arguments:
  keyword               The keyword you want to search for

options:
  -h, --help            show this help message and exit
  -s SEARCH_ENGINE, --search-engine SEARCH_ENGINE
                        Your preferred search engine for search
  -b BROWSER, --browser BROWSER
                        Your preferred browser to search
  -t TYPE, --type TYPE  The media type that your would like to search for: web, image, video
  -a, --all             Flag to indicate that you want to search on all compatible search engines
  --change-default      Flag to indicate that you want to edit the default config file
  --display-default     Flag to indicate that you want to review the default config
  --show-functions      Flag to display all compatible seatch engines & their options
```
Beware that :
- Not all file types (as specified by -a flag) is compatible with all listed serach engines. You can refer to their compatibilities in the [Allowed Options](#allowed-options) section.
- The default type of search is `web`, you don't need to specify the search type using `-t, --type` if you are performing web search.
- The `-a, --all` flags allow user to search for the same keyword and type on all compatible sites that are listed in the search engine. When `-a` flag is set, users do not need to set additional `-s, --search-eingine` flag.

## Search Engines
There are a list of supported search engines listed in `config/search_engines.json`. The definition follows the following syntax:
```
[Name of Search Engine]: {
    (Optional) "web": {
      "base-url": <Base URL for web search>,
      "query-params" : {
        "keyword": <Query param appended before keyword>
      },
      "direct": <true / false>
    },
    (Optional) "image" {
      "base-url": <Base URL for image search>,
      "query-params": {
        "keyword": <Query param appended before keyword>
      },
      "direct": <true / false>
    },
    (Optional) "video": {
      "base-url": <Base URL for image search>,
      "query-params": {
        "keyword": <Query param appended before keyword>
      },
      "direct": <true / false>
    }
  },
```
Note that:
- Not all types of search is compatible with all listed search engines (e.g., Google supports all three types of searches - `web`, `image`, `video`, while Youtube only supports `video` search)
- The `direct` flag is used to indicate whether the search can be executed by directly appending query parameters to the URL. If  `direct` is set to `true`, the URL will be formulated before launching the webdriver. If `direct` is set to `false`, the additional paramters will be formulated as a keyword (e.g., concatenating additional information with spaces), and the URL is formed using the new keyword

## Allowed Options
The list of supported options (including browsers and search engines) are listed in `config/allowed_options.json`. The definition follows the following syntax:
```
"browsers": [List of supported browsers],
  "search_engines": [
    {
      "name": <Name of search engine>,
      "methods": ["web", "image", "video"]
    },
    ...
  ]
```
If you want to add additional search engines, make sure you add the search engine in `config/allowed_options.json` file for it to be correctly identified by the program.

## Default
The default configuration is stored in `config/default.json`. In this file, you can specify your preferred browser and your preferred search engine for each type of searches (`web`, `video`, `image`). The syntax is as follows:
```
{
    "browser": <browser names as listed in allowed_options>,
    "se": {
        "web": <preferred search engine for web>,
        "video": <preferred search engine for video>,
        "image": <preferred search engine for image>
    }
}
```
You can directly change your default setting by editting the `config/default.json` file.

Note that:
- Make sure that the name that you are exactly the same as what is displayed in `allowed_options.json`.
- When `search` is launched, it will automatically load your default settings. Therefore, if you have default configurations available in `default.json`, you simply need to specify the `-w` flag to specify the keyword. 
- As stated in [flags section](#flags), the default search type (specified by `-t, --type`) is `web`. You need to explicitly indicate the type if you want to override this, 

## Browser Commands
The os-specific commands that will be used to launch a browser from terminal are listed in `config/browser.json` in following structure:
```
{
    "default": {
        <OS>: ["command", "to", "launch", "default", "browser"],
    },
    <Browser>: {
        <OS>: ["command", "to", "launch", "specific", "browser", "from", "OS"],
        ...
    },
    ...
}
```
If the browser specified in command is not available in your system, the search will be launched using the default browser that is configured in the system.

# Examples
The following are some examples to demonstrate how to use the command line tool.
## Scenario: Default Not Set: 
### Search for web content about "github" on Google using Chrome
  ```
  search -w github -s google -b chrome
  ```  
  Notice that `-t web` is dropped because web search is the default type of search.

### Search for video content about "python" on YouTube using Firefox
  ```
  search -w python -s youtube -b firefox -t video
  ```
  In this case, since the search type is not `web`, need to explicitly specify it using `-t` flag
### Search for image content about "DS&A" on all compatible search engines using Chrome
  ```
  search -w "data structure and algorithm" -a -b chrome -t image
  ```
  In this case, all search engines that supports `image` type of search will be launched.
## Scenario: Default Set
The command line tool comes with a `default.json` file for simplicity of use. Here is the structure of the configuration:
```
{
    "browser": "firefox",
    "se": {
        "web": "GOOGLE",
        "video": "YOUTUBE",
        "image": "PINTEREST"
    }
}
```
Note that, if the `default.json` configuration file is changed, you need to [rebuild and install](#installation) the tool in your current environment.
### Search for web content about "programming language" on Google using Firefox
```
search -w "programming language"
```
Note that since 1) the default search type is `web`, 2) `google` is the default search engine for web based content 3) `firefox` is the default browser, only the keyword parameter is required.
### Search for video content about "java" on YouTube using Chrome
```
search -w java -t video -b chrome
```
Note that `youtube` is the default search engine used for `video`, the `-s, --search-engine` flag is dropped.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
