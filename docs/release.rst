====================================
How to release a new Devilry version
====================================

In the devilry-django repo:

1. Update the version number in ``src/devilry/setup.py`` and ``src/devilry/devilry/version.py``
2. Update the version number in ``docs/conf.py``.
3. Commit the version changes.
4. Tag the release::

    $ git tag vX.Y.Z

5. Push the changes::

    $ git push
    $ git push --tags


In the devilry-deploy repo:

1. Update the version number in ``docs/src/conf.py``
2. Update the revision id in ``${buildout:extends}`` and
   ``${download-devilryrepo}`` in ``buildout/buildout-base.cfg``. Must use TAG,
   not branch name.
3. Tag the release and push just like you did for devilry-django above.


In the devilry-userdoc repo (this is not needed for RC and Beta releases):

1. Update the version number in ``conf.py``
2. Tag the release and push just like you did for devilry-django above.


.. note:: We plan on making this more streamlined in the future --- see :devilryissue:`384`.
