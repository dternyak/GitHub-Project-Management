# GitHub-Project-Management

This tool is meant to be used as a utility for managing projects on GitHub.

There are two main functionalities offered by the utility:

1. Get a list of commits (with auto-paging if needed) on a tree since a sha-hash. This is useful for tracking progress between releases.
    - Ex: `python main.py --repo=myetherwallet --org=myetherwallet --branch=master --since-sha=cba5672 --utility=release`
    ```
    ---------------------------------------
    Showing commits merged into develop after: cba5672
    ---------------------------------------
    Total Merged PRs: 41
    ---------------------------------------
    message: Fix Missing Address in Paper Wallet (#292)
    author: Daniel Ternyak
    date: 2017-10-14
    
    message: Deprecate Docker Support (#290)
    author: Daniel Ternyak
    date: 2017-10-14
    ...
    ```
2. Get an output of assigned issues during a sprint (sprint issues are measured by issues belonging to a certain milestone number).
    - Ex: `python main.py --repo=myetherwallet --org=myetherwallet --utility=sprint --sprint=4`
    ```
    Here are the tasks for sprint 4.

    *Daniel Ternyak*
    Don't store Bity Rates in Local Storage: (https://github.com/MyEtherWallet/MyEtherWallet/issues/392)
    Add Send Tooltips: (https://github.com/MyEtherWallet/MyEtherWallet/issues/343)
    
    *Joe Bob*
    ... 
      ```
To get started:

1. Clone the repo
2. (Optional -- enables a higher rate limit from GitHub) Adjust the app client secret in config.py
3. `pip install -r requirements.txt`
4. Run your preferred report! 
