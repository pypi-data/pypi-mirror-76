#####################
Documatt Sphinx Theme
#####################

This Sphinx theme was designed to provide great reading documentation experience. This theme is default theme of `Documatt.com <https://documatt.com>`_ projects but you are welcome to use it with any Sphinx project.

TIP: To see theme in action visit for example https://blog.documatt.com.

.. absolute image URL because it will be embedded also to PyPI

.. image:: https://gitlab.com/documatt/sphinx-themes/-/raw/master/sphinx_documatt_theme/screenshot.png?inline=false

************
Installation
************

Install (on the commandline)::

    $ pip install sphinx-documatt-theme

Use it (in your ``conf.py``)::

    html_theme = "sphinx_documatt_theme"

*************
Configuration
*************

Theme as only option - set "motto" displayed by default in the cover (block bellow breadcrumb near header), and in the footer. Set your very own motto::

    html_theme_options = {
        "motto": "Write and read beautiful books and documentation in easy way with our powerful writing platform."
    }

