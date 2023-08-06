Release History
===============

**2.3.1 2020-08-12**

*   fixed a bug where reading the config file failed once Tenant information
    has been propagated, due variations in the timestamps format created by
    various HCP versions

**2.3.0 2017-06-26**

*   added option '-f INFILE' to enable reading chargeback data from a file
    downloaded from the Management User Interface

**2.2.1 2017-05-24**

*   Removed the dependency for Python 3.5 - now works with Python 3.4

**2.2.0 2017-05-23**

*   Re-factored the code to allow for binary creation using pyinstaller

**2.1.4 2016-01-12**

*   Fixed:

    *   A bug that caused the tool to fail while having no access to a Tenant

**2.1.3 2016-01-11**

*   Fixed:

    *   A bug that caused chart creation to fail in case at least one Tenant
        was disabled for report collection
    *   Another bug that cause the tool to fail if no report data is available
        at all


**2.1.2 2016-01-09**

*   Added:

    *   Ability to 'switch off' Tenants from collection (config file)
    *   Ability to just update the Tenant list w/o collection (``-u``)
    *   Ability to generate charts without downloading reports (``-c``)
    *   Ability to start collection defineable days in the past - once for each
        Tenant that was not collected before (``--pastdays``)

**2.1.1 2016-01-07**

*   Documentation fixes

**2.1.0 2016-01-06**

*   Added:

    Chart creation

*   Fixed:

    Report file names (removed ':'s to make sure not to conflict with Windows
    rules)

**2.0.1 2016-01-01**

*   Changed:

    *   rebuilt from scratch to get rid of the sqlite3 database used in
        version 1.x
    *   now using the hcpsdk
    *   now storing the reports in a folder structure
    *   added possibility to store to HCP

