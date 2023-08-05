# Copyright (C) 2012-2013 by Łukasz Langa
# Copyright (C) 2020 by Nguyễn Hồng Quân
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from functools import partial


unset = object()
gettext = unset
no_id_given = -255


class ChoicesEntry(int):
    global_id = 0

    def __new__(cls, *args, **kwargs):
        return super(ChoicesEntry, cls).__new__(
            cls, kwargs['id']
        )

    def __init__(self, description, id, name=None):
        self.raw = description
        self.global_id = ChoicesEntry.global_id
        self.name = name
        self.__extra__ = []
        ChoicesEntry.global_id += 1

    @property
    def desc(self):
        if not self.raw:
            return self.raw
        # gettext obscured that way so you can use choices in settings.py
        global gettext
        if gettext is unset:
            from django.utils.translation import gettext
        return gettext(self.raw)

    @property
    def id(self):
        return int(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value.strip('_') if value else value
        self.__raw_name = value

    def __str__(self):
        name = self.name
        return "<{}: {} (id: {})>".format(self.__class__.__name__,
                                          name, self.id)

    def __repr__(self):
        name = self.name
        name = "{!r}".format(name)
        if name[0] in 'bru':
            name = name[2:-1]
        else:
            name = name[1:-1]
        return "<{}: {} (id: {})>".format(self.__class__.__name__,
                                          name, self.id)

    def extra(self, **other):
        """Enables adding custom attributes to choices at declaration time.
        For example::

            class Color(Choices):
                _ = Choices.Choice

                red = _("red").extra(html='#ff0000')
                green = _("green").extra(html='#00ff00')
                blue = _("blue").extra(html='#0000ff')

        Later on you can use the defined attribute directly::

            >>> Color.red.html
            '#ff0000'

        or with choices received using the getters::

            >>> Color.from_name(request.POST['color']).html
            '#00ff00'
        """
        for key, value in other.items():
            self.__extra__.append(key)
            setattr(self, key, value)
        return self


class ChoiceGroup(ChoicesEntry):
    """A group of choices."""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, id=kwargs.get('id', args[0]))

    def __init__(self, id, description=''):
        super(ChoiceGroup, self).__init__(description, id=id)
        self.choices = []


class Choice(ChoicesEntry):
    """A single choice."""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, id=kwargs.get('id', no_id_given))

    def __init__(self, description, id=no_id_given, name=None):
        super(Choice, self).__init__(description, id=id, name=name)
        self.group = None

    def __str__(self):
        return self.desc

    def __repr__(self):
        rawval = self.raw
        name = "{!r}".format(self.name)
        if name[0] in 'bru':
            name = name[2:-1]
        else:
            name = name[1:-1]
        rawval = "{!r}".format(rawval)
        if rawval[0] in 'bru':
            rawval = rawval[2:-1]
        else:
            rawval = rawval[1:-1]
        result = "<{}: {} (id: {}, name: {})>".format(self.__class__.__name__,
                                                      rawval, self.id, name)
        return result


def _getter(name, given, returns, found, getter):

    def impl(cls, id, found=lambda id, k, v: False,
             getter=lambda id, k, v: None, fallback=unset):
        """Unless `fallback` is set, raises ValueError if name not present."""
        for k, v in cls.__dict__.items():
            if isinstance(v, ChoicesEntry) and found(id, k, v):
                return getter(id, k, v)
        if fallback is unset:
            raise ValueError("Nothing found for '{}'.".format(id))
        else:
            return fallback

    function = partial(impl, found=found, getter=getter)
    function.__name__ = name
    function.__doc__ = (
        "Choices.{name}({given}, fallback=unset) -> {returns}"
        "\n\nGiven the `{given}`, returns the `{returns}`. {impl_doc}"
        .format(name=name, given=given, returns=returns,
                impl_doc=impl.__doc__)
    )
    return classmethod(function)


class _ChoicesMeta(type):
    def __new__(meta, classname, bases, class_dict):
        groups = []
        values = []
        raw_values = []
        for k, v in class_dict.items():
            if not isinstance(v, ChoicesEntry):
                continue
            v.name = k
            raw_values.append(v)
        raw_values.sort(key=lambda elem: elem.global_id)
        last_choice_id = 0
        group = None
        for choice in raw_values:
            if isinstance(choice, ChoiceGroup):
                last_choice_id = choice.id
                group = choice
                groups.append(group)
            else:
                if choice.id == no_id_given:
                    last_choice_id += 1
                    c = Choice(choice.raw, id=last_choice_id,
                               name=choice.name)
                    d = dict(((k, getattr(choice, k)) for k in
                              choice.__extra__))
                    choice = c.extra(**d)
                last_choice_id = choice.id
                if group is not None:
                    group.choices.append(choice)
                    choice.group = group
                    d = dict(((k, getattr(group, k)) for k in
                              group.__extra__ if k not in choice.__extra__))
                    choice.extra(**d)
                values.append(choice)
                class_dict[choice._ChoicesEntry__raw_name] = choice
        class_dict['__groups__'] = groups
        class_dict['__choices__'] = values
        return type.__new__(meta, classname, bases, class_dict)


class Choices(list, metaclass=_ChoicesMeta):
    def __init__(self, filter=(unset,), item=unset, grouped=False):
        """Creates a list of pairs from the specified Choices class.
        By default, each pair consists of a numeric ID and the translated
        description. If `use_ids` is False, the name of the attribute
        is used instead of the numeric ID.

        If `filter` is specified, it's a set or sequence of attribute
        names that should be included in the list. Note that the numeric
        IDs are the same regardless of the filtering. This is useful
        for predefining a large set of possible values and filtering to
        only the ones which are currently implemented."""
        if not self.__choices__:
            raise ValueError("Choices class declared with no actual "
                             "choice fields.")
        if item is unset:
            def item(choice):
                return (choice.id, choice.desc)
        filter = set(filter)
        if grouped and self.__groups__:
            for group in self.__groups__:
                group_choices = []
                for choice in group.choices:
                    if (choice.name in filter
                            or (unset in filter and isinstance(choice, Choice))):   # NOQA: W503
                        group_choices.append(item(choice))
                if group_choices:
                    self.append((group.desc, tuple(group_choices)))
        else:
            if grouped:
                import warnings
                warnings.warn("Choices class called with grouped=True and no "
                              "actual groups.")
            for choice in self.__choices__:
                if (choice.name in filter
                        or (unset in filter and isinstance(choice, Choice))):  # NOQA: W503
                    self.append(item(choice))

    from_name = _getter(
        "from_name",
        given="name",
        returns="choice object",
        found=lambda id, k, v: k == id,
        getter=lambda id, k, v: v
    )

    id_from_name = _getter(
        "id_from_name",
        given="name",
        returns="id",
        found=lambda id, k, v: k == id,
        getter=lambda id, k, v: v.id
    )

    desc_from_name = _getter(
        "desc_from_name",
        given="name",
        returns="localized description string",
        found=lambda id, k, v: k == id,
        getter=lambda id, k, v: v.desc
    )

    raw_from_name = _getter(
        "raw_from_name",
        given="name",
        returns="raw description string",
        found=lambda id, k, v: k == id,
        getter=lambda id, k, v: v.raw
    )

    from_id = _getter(
        "from_id",
        given="id",
        returns="choice object",
        found=lambda id, k, v: v.id == id,
        getter=lambda id, k, v: v
    )

    name_from_id = _getter(
        "name_from_id",
        given="id",
        returns="attribute name",
        found=lambda id, k, v: v.id == id,
        getter=lambda id, k, v: k
    )

    desc_from_id = _getter(
        "desc_from_id",
        given="id",
        returns="localized description string",
        found=lambda id, k, v: v.id == id,
        getter=lambda id, k, v: v.desc
    )

    raw_from_id = _getter(
        "raw_from_id",
        given="id",
        returns="raw description string",
        found=lambda id, k, v: v.id == id,
        getter=lambda id, k, v: v.raw
    )

    @staticmethod
    def to_ids(func):
        """Converts a sequence of choices to a sequence of choice IDs."""
        def wrapper(self):
            return (elem.id for elem in func(self))
        return wrapper

    @staticmethod
    def to_names(func):
        """Converts a sequence of choices to a sequence of choice names."""
        def wrapper(self):
            return (elem.name for elem in func(self))
        return wrapper

    Choice = Choice
    Group = ChoiceGroup
