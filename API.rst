***
API
***

========
workflow
========

Assuming that :file:`et-micc-dev` is the current working directory:

#. Make sure that there are no untracked files in et-micc and et-micc-build that 
   need to be added to the respective git repositories.
#. Execute

   .. code-block:: bash
   
      > bumpversion --config-file .bumpversion.cfg major|minor|patch
   
   This will bump the versions in:
   
   * et-micc/pyproject.toml
   * et-micc/et_micc/__init__.py
   * et-micc-build/pyproject.toml
   
   Note that, normally, you run bumpversion in the project directory, and that
   it will check if the git repo is clean. Here, it will  

#. Execute

   .. code-block:: bash
   
      > cd ../et-micc       && poetry publish --build 
      > cd ../et-micc-build && poetry publish --build 
      
      
==============
implementation
==============

Implementation is based on:

* `bump2version <https://github.com/c4urself/bump2version>`_
* `pygit2 <https://www.pygit2.org/repository.html>`_

Pygit2_ requires libgit2 which was installed system wide using 
`these instructions <https://www.pygit2.org/install.html#install-libgit2-from-source>`_

.. automodule:: et_micc_dev
   :members:
