The MgeFit Package
==================

**MgeFit: Multi-Gaussian Expansion Fitting of Galactic Images**

.. image:: https://img.shields.io/pypi/v/mgefit.svg
        :target: https://pypi.org/project/mgefit/
.. image:: https://img.shields.io/badge/arXiv-astroph:0201430-orange.svg
        :target: https://arxiv.org/abs/astro-ph/0201430
.. image:: https://img.shields.io/badge/DOI-10.1046/...-green.svg
        :target: https://doi.org/10.1046/j.1365-8711.2002.05412.x

MgeFit is a Python implementation of the robust and efficient Multi-Gaussian
Expansion (MGE) fitting algorithm for galactic images of `Cappellari (2002)
<https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C>`_.

Attribution
-----------

If you use this software for your research, please cite
`Cappellari (2002) <https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C>`_.
The BibTeX entry for the paper is::

    @Article{Cappellari2002,
        author = {{Cappellari}, M.},
        title = {Efficient multi-Gaussian expansion of galaxies},
        journal = {MNRAS},
        eprint = {arXiv:astro-ph/0201430}
        year = {2002},
        volume = {333},
        pages = {400-410},
        doi = {10.1046/j.1365-8711.2002.05412.x}
    }


Installation
------------

install with::

    pip install mgefit

Without writing access to the global ``site-packages`` directory, use::

    pip install --user mgefit

Documentation
-------------

See ``mgefit/examples`` and the files headers.

License
-------

Copyright (c) 1999-2020 Michele Cappellari

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included in all
copies of the software. All other rights are reserved.
In particular, redistribution of the code is not allowed.

