==========
dj.choicee
==========

.. image:: https://badgen.net/pypi/v/dj.choicee
   :target: https://pypi.org/project/dj.choicee
.. image:: https://travis-ci.org/AgriConnect/dj.choicee.png
  :target: https://travis-ci.org/AgriConnect/dj.choicee

This is a much clearer way to specify choices for fields in models and forms.
A basic example:

.. code-block:: python

    >>> from dj.choicee import Choices
    >>> class Gender(Choices):
    ...   _ = Choices.Choice
    ...
    ...   male = _("Male")
    ...   female = _("Female")
    ...
    >>> Gender()
    [(1, 'Male'), (2, 'Female')]
    >>> Gender.male
    <Choice: male (id: 1)>
    >>> Gender.female
    <Choice: female (id: 2)>
    >>> Gender.male.id
    1
    >>> Gender.male.desc
    'Male'
    >>> Gender.male.raw
    'Male'
    >>> Gender.male.name
    'male'
    >>> Gender.from_name("male")
    <Choice: male (id: 1)>
    >>> Gender.id_from_name("male")
    1
    >>> Gender.raw_from_name("male")
    'Male'
    >>> Gender.desc_from_name("male")
    'Male'
    >>> Gender.name_from_id(2)
    'female'
    >>> Gender.name_from_id(3)
    Traceback (most recent call last):
    ...
    ValueError: Nothing found for '3'.
    >>> Gender.from_name("perez")
    Traceback (most recent call last):
    ...
    ValueError: Nothing found for 'perez'.

You define a class of choices, specifying each choice as a class attribute.
Those attributes are ``int`` subclasses, numbered automatically starting with
1.  The class provides several features which support the DRY principle:

 * An object instantiated from the choices class is basically a list of ``(id,
   localized_description)`` pairs straight for consumption by Django.

 * Each attribute defined can be retrieved directly from the class.

 * Metadata (e.g. attribute name, raw and localized description, numeric ID) of
   each attribute is accessible.

 * Choices which are suffixed by ``_`` to avoid clashing with Python keywords
   have this suffix automatically removed in their ``.name`` attributes

 * Lookup functions are available to help getting attributes or their metadata.

..  note::
    The ``_ = Choices.Choice`` trick makes it possible for ``django-admin.py
    makemessages`` to find each choice description and include it in ``.po``
    files for localization.  It masks ``gettext`` only in the scope of the class so
    the rest of the module can safely use ``gettext`` or ``gettext_lazy``.  Having to
    specify ``_`` each time is not a particularly pretty solution but it's
    explicit. Suggestions for a better approach are welcome.

Grouping choices
----------------

One of the worst problems with choices is their weak extensibility.  For
instance, an application defines a group of possible choices like this:

.. code-block:: python

    >>> class License(Choices):
    ...   _ = Choices.Choice
    ...
    ...   gpl = _("GPL")
    ...   bsd = _("BSD")
    ...   proprietary = _("Proprietary")
    ...
    >>> License()
    [(1, 'GPL'), (2, 'BSD'), (3, 'Proprietary')]

All is well until the application goes live and after a while the developer
wants to include LGPL.  The natural choice would be to add it after ``gpl`` but
when we do that, the indexing would break.  On the other hand, adding the new
entry at the end of the definition looks ugly and makes the resulting combo
boxes in the UI sorted in a counter-intuitive way.  Grouping lets us solve this
problem by explicitly defining the structure within a class of choices:

.. code-block:: python

    >>> class License(Choices):
    ...   _ = Choices.Choice
    ...
    ...   COPYLEFT = Choices.Group(0)
    ...   gpl = _("GPL")
    ...
    ...   PUBLIC_DOMAIN = Choices.Group(100)
    ...   bsd = _("BSD")
    ...
    ...   OSS = Choices.Group(200)
    ...   apache2 = _("Apache 2")
    ...
    ...   COMMERCIAL = Choices.Group(300)
    ...   proprietary = _("Proprietary")
    ...
    >>> License()
    [(1, 'GPL'), (101, 'BSD'), (201, 'Apache 2'), (301, 'Proprietary')]

This enables the developer to include more licenses of each group later on:

.. code-block:: python

    >>> class License(Choices):
    ...   _ = Choices.Choice
    ...
    ...   COPYLEFT = Choices.Group(0)
    ...   gpl_any = _("GPL, any")
    ...   gpl2 = _("GPL 2")
    ...   gpl3 = _("GPL 3")
    ...   lgpl = _("LGPL")
    ...   agpl = _("Affero GPL")
    ...
    ...   PUBLIC_DOMAIN = Choices.Group(100)
    ...   bsd = _("BSD")
    ...   public_domain = _("Public domain")
    ...
    ...   OSS = Choices.Group(200)
    ...   apache2 = _("Apache 2")
    ...   mozilla = _("MPL")
    ...
    ...   COMMERCIAL = Choices.Group(300)
    ...   proprietary = _("Proprietary")
    ...
    >>> License()
    [(1, 'GPL, any'), (2, 'GPL 2'), (3, 'GPL 3'), (4, 'LGPL'),
     (5, 'Affero GPL'), (101, 'BSD'), (102, 'Public domain'),
     (201, 'Apache 2'), (202, 'MPL'), (301, 'Proprietary')]

Note the behaviour:

 * the developer renamed the GPL choice but its meaning and ID remained stable

 * BSD, Apache and proprietary choices have their IDs unchanged

 * the resulting class is self-descriptive, readable and extensible

As a bonus, the explicitly specified groups can be used when needed:

.. code-block:: python

    >>> License.COPYLEFT
    <ChoiceGroup: COPYLEFT (id: 0)>
    >>> License.gpl2 in License.COPYLEFT.choices
    True
    >>> [(c.id, c.desc) for c in License.COPYLEFT.choices]
    [(1, 'GPL, any'), (2, 'GPL 2'), (3, 'GPL 3'), (4, 'LGPL'),
     (5, 'Affero GPL')]

``ChoiceField``
---------------

Choices can be used with generic ``IntegerField`` and ``CharField`` instances.
When you do that though, some minor API deficiencies show up fairly quickly.
First, when you define the field, you have to instanciate the choices class and
the default value has to be converted to the proper type explicitly:

.. code-block:: python

    color = models.IntegerField(choices=Color(), default=Color.green.id)

Second, when getting the attribute back from a model, it has to be converted to
a ``Choice`` instance to do anything interesting with it:

.. code-block:: python

    >>> obj = Model.objects.get(pk=3)
    >>> obj.color
    3
    >>> Color.from_id(obj.color)
    <Choice: Blue (id: 3, name: blue)>

To overcome those problems a ``ChoiceField`` is available in the
``dj.choicee.fields`` package.  It is based on integers on the database level but
the API exposes ``Choice`` instances.  This helps both on the definition side:

.. code-block:: python

    color = ChoiceField(choices=Color, default=Color.green)

and on the access side:

.. code-block:: python

    >>> obj = Model.objects.get(pk=3)
    >>> obj.color
    <Choice: Blue (id: 3, name: blue)>
    >>> obj.color = Color.green
    >>> obj.save()
    >>> Model.objects.get(pk=3).color
    <Choice: Green (id: 2, name: green)>

For rendering forms, the field coerces to integer values.  That also means that
wherever ``Choice`` instances are accepted, integers are also fine.

Advanced functionality
----------------------

Filtering
~~~~~~~~~

The developer can specify all possible choices for future use and then filter
out only the currently applicable values on choices creation:

.. code-block:: python

    >>> class Language(Choices):
    ...   _ = Choices.Choice
    ...
    ...   de = _("German")
    ...   en = _("English")
    ...   fr = _("French")
    ...   pl = _("Polish")
    ...
    >>> Language()
    [(1, 'German'), (2, 'English'), (3, 'French'), (4, 'Polish')]
    >>> Language(filter=("en", "pl"))
    [(2, 'English'), (4, 'Polish')]

This has the great advantage of keeping the IDs and sorting intact.

Custom item format
~~~~~~~~~~~~~~~~~~

One can also change how the pairs are constructed by providing a factory
function.  For instance, to use the class of choices defined above for the
``LANGUAGES`` setting in ``settings.py``, one could specify:

.. code-block:: python

    >>> Language(item=lambda choice: (choice.name, choice.raw))
    [('de', 'German'), ('en', 'English'), ('fr', 'French'),
     ('pl', 'Polish')]

Extra attributes on choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each choice can receive extra arguments using the ``extra()`` method:

.. code-block:: python

    >>> class Python(Choices):
    ...   _ = Choices.Choice
    ...
    ...   cpython = _("CPython").extra(language='C')
    ...   pypy = _("PyPy").extra(language='Python')
    ...   jython = _("Jython").extra(language='Java')
    ...   iron_python = _("IronPython").extra(language='C#')

This adds a ``language`` attribute to each choice so you can get it back like
this:

.. code-block:: python

    >>> Python.jython.language
    'Java'

This enables polymorphic attribute access later on when using models or forms.
For instance, suppose you have a simple model like:

.. code-block:: python

    >>> class Library(models.Model):
    ...   name = models.CharField(max_length=100)
    ...   python_kind = models.IntegerField(choices=Python(), default=Python.cpython.id)

In that case to get the implementation language back yo'd do:

.. code-block:: python

    >>> library = Library.objects.get(name='dj.choicee')
    >>> Python.from_id(library.python_kind).language
    'C'

That frees your user code of any conditionals or dictionaries that depend on the
state of the choices class.  If you would add another choice to it, no user code
needs to be changed to support it.  This also supports the DRY principle because
the choices class becomes the single place where configuration of that kind is
held.

Extra attributes on choice groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unsurprisingly, choice groups can have extra attributes as well.  They are then
inherited by choices in such a group and can be overriden if necessary.  For
instance:

.. code-block:: python

  >>> class ProfileChange(Choices):
  ...   _ = Choices.Choice
  ...
  ...   USER = Choices.Group(0).extra(icon='bookkeeping.png', is_public=True)
  ...   email = _("e-mail").extra(is_public=False)
  ...   first_name = _("first name")
  ...   last_name = _("last name")
  ...
  ...   BASIC_INFO = Choices.Group(10).extra(icon='bookkeeping.png', is_public=True)
  ...   birth_date = _("birth date").extra(icon='calendar.png')
  ...   gender = _("gender").extra(icon='male_female.png')
  ...   country = _("country")
  ...   city = _("city")
  ...
  ...   CONTACT_INFO = Choices.Group(20).extra(icon='contactbook.png', is_public=False)
  ...   skype = _("Skype ID")
  ...   icq = _("ICQ number")
  ...   msn = _("MSN login")
  ...   xfire = _("X-Fire login")
  ...   irc = _("IRC info").extra(is_public=True)

In that case proper inheritance takes place:

.. code-block:: python

  >>> ProfileChange.first_name.is_public
  True
  >>> ProfileChange.email.is_public
  False
  >>> ProfileChange.country.icon
  'bookkeeping.png'
  >>> ProfileChange.birth_date.icon
  'calendar.png'


Predefined choices
------------------

There are several classes of choices which are very common in web applications
so they are provided already: ``Country``, ``Gender`` and ``Language``.

How do I run the tests?
-----------------------

Install `tox <https://pypi.org/project/tox/>`_ then run:

.. code-block:: sh

  $ tox -e py

Change Log
----------

1.0.0
~~~~~

* Pure Python 3 (drop Python 2 compatibility).
* Support only Python3.5+ and Django 2.0+
* Fork from `dj.choices`_ to new project.

Authors
-------

- Original `dj.choices`_ author `Łukasz Langa <mailto:lukasz@langa.pl>`_.
- Fork and drop legacy Python2 code: `Nguyễn Hồng Quân <ng.hong.quan@gmail.com>`_.


.. _dj.choices: https://pypi.org/project/dj.choices/
