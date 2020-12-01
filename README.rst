===========
et-micc-dev
===========

we want to publish et-micc_ and et-micc-build_ together, with the same version. The
script :file:`../et_micc_dev/cli_publish.py` takes care of that.

#. Verify that the repos of et-micc and et-micc-build are clean.
#. Bump the version number

Scripts for maintaining and publishing et-micc and et-micc-build.

* `PyPI et-micc <https://pypi.org/project/et-micc/>`_ 
* `PyPI et-micc-build <https://pypi.org/project/et-micc-build/>`_ 
* `github et-micc <https://github.com/etijskens/et-micc>`_ 
* `github et-micc-build <https://github.com/etijskens/et-micc-build>`_

.. note:: The virtual environment of et-micc-dev was set up manually
   because poetry fails at installing pygit2.

Use this (and only this) to publish et-micc and et-micc-build:

.. code-block:: bash

    > cd path/to/et-micc-dev
    > . activenv
    (.venv) > python et_micc_dev/cli_publish.py <rule>
    ...

Here, ``<rule>`` is any valid semver_ rule. The default is `patch`
