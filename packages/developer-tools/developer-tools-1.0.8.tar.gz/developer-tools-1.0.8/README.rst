developer-tools
===============

Useful tools for Python developers.

This is mostly an example to show how `autopip <https://pypi.org/project/autopip/>`_ can be used to install a group of
apps with various version specifications, but the author does install it as it conveniently provides all the tools
useful for doing Python software development.

To tell `autopip` to install other apps, simply add an `autopip` entry point group in ``setup.py`` with the list of
apps and versions. Versions can be pinned to major or a specific version, or use `latest` to install the latest version.
Update frequency can also be specified per app. See working example of `autopip` entry point group
in `developer-tools' setup.py <https://github.com/maxzheng/developer-tools/blob/master/setup.py#L27>`_::

    entry_points={
        'autopip': [
            'ansible = 2.5.4',                 # Pin to specific version without auto-update (recommended for 3rd party)
            'ansible-hostmanager = latest',    # Install latest and update hourly (for apps that you own)
            'awscli = 1.15 [monthly]',         # Pin to minor and update monthly
            'flake8 = 3 [weekly]',             # Pin to major and update weekly
            'twine = 1 [weekly]',
            'rstcheck = 3.0.1',
            'workspace-tools = latest',
        ],
    },

For better security and user experience, it is recommended to pin to a specific version -- at least minor -- for 3rd
party apps. For apps that you own where you have good versioning in the app, then `latest` works better to let the app
control its own release.

Seeing is believing, so try installing it::

    autopip install developer-tools

Which should output something like the following -- line 3 is the interesting part::

    Installing developer-tools to /home/mzheng/.apps/developer-tools/0.0.3
    Hourly auto-update enabled via cron service
    This app has defined "autopip" entry points to install: ansible==2.5.4 ... twine==1.* workspace-tools
    Installing ansible to /home/mzheng/.apps/ansible/2.5.4
    Updating script symlinks in /home/mzheng/.apps/bin
    + ansible
    ...
    ...
    Installing workspace-tools to /home/mzheng/.apps/workspace-tools/3.2.4
    Hourly auto-update enabled via cron service
    Updating script symlinks in /home/mzheng/.apps/bin
    + wst

And everything is installed as expected:

.. code-block:: console

    $ autopip list
    ansible              2.5.4    /home/mzheng/.apps/ansible/2.5.4
    ansible-hostmanager  0.2.3    /home/mzheng/.apps/ansible-hostmanager/0.2.3  [updates hourly]
    awscli               1.15.31  /home/mzheng/.apps/awscli/1.15.31             [updates monthly]
    developer-tools      1.0.1    /home/mzheng/.apps/developer-tools/1.0.1      [updates hourly]
    flake8               3.5.0    /home/mzheng/.apps/flake8/3.5.0               [updates weekly]
    rstcheck             3.0.1    /home/mzheng/.apps/rstcheck/3.0.1
    twine                1.11.0   /home/mzheng/.apps/twine/1.11.0               [updates weekly]
    workspace-tools      3.2.4    /home/mzheng/.apps/workspace-tools/3.2.4      [updates hourly]

Finally, uninstall will remove them all as well -- though I do recommend keeping them:

.. code-block:: console

    $ app uninstall developer-tools
    Uninstalling developer-tools
    This app has defined "autopip" entry points to uninstall: ansible ... workspace-tools
    Uninstalling ansible
    Uninstalling ansible-hostmanager
    Uninstalling awscli
    Uninstalling flake8
    Uninstalling rstcheck
    Uninstalling twine
    Uninstalling workspace-tools

Pretty cool, huh? :)


Links & Contact Info
====================

| PyPI Package: https://pypi.python.org/pypi/developer-tools
| GitHub Source: https://github.com/maxzheng/developer-tools
| Report Issues/Bugs: https://github.com/maxzheng/developer-tools/issues
|
| Follow: https://twitter.com/MaxZhengX
| Connect: https://www.linkedin.com/in/maxzheng
| Contact: maxzheng.os @t gmail.com
