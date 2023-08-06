#!/usr/bin/env python3

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

import math

from django import forms
from django.core import exceptions, validators
from django.db.models.fields import IntegerField
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from .core import unset, Choices


class ChoiceField(IntegerField):
    description = _("Integer")

    def __init__(self, *args, **kwargs):
        if 'choices' not in kwargs or not isinstance(kwargs['choices'], type):
            raise exceptions.ImproperlyConfigured("No choices class specified.")
        else:
            try:
                if not issubclass(kwargs['choices'], Choices):
                    raise TypeError()
            except TypeError:
                raise exceptions.ImproperlyConfigured(
                    "dj.choicee class required as `choices` argument."
                )
        self.choice_class = kwargs['choices']
        self.item_getter = kwargs.get('item', lambda x: (x.id,))
        kwargs['choices'] = self.choice_class(
            item=kwargs.get('item', unset),
            filter=kwargs.get('filter', (unset,)),
            grouped=kwargs.get('grouped', False)
        )
        if isinstance(kwargs.get('default'), Choices.Choice):
            kwargs['default'] = self.item_getter(kwargs['default'])[0]
        nkwargs = {k: kwargs[k] for k in kwargs if k not in ('filter', 'grouped', 'item')}
        super().__init__(*args, **nkwargs)

    def to_python(self, value):
        value = super().to_python(self.get_prep_value(value))
        if value is None:
            return value
        try:
            return self.choice_class.from_id(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'] % {'value': value}
            )

    def from_db_value(self, value, expression, connection, context=None):
        # "context" is removed in Django 3.0
        if value is None:
            return value
        return self.choice_class.from_id(value)

    def from_python(self, value):
        return self.get_prep_value(self.to_python(value))

    def get_prep_value(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, (str, int)):
            return int(value)
        return self.item_getter(value)[0]

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('exact', 'lt', 'lte', 'gt', 'gte'):
            if lookup_type in ('gte', 'lt') and isinstance(value, float):
                value = math.ceil(value)
            else:
                value = self.get_prep_value(value)
        elif lookup_type in ('in', 'range'):
            value = [self.get_prep_value(v) for v in value]
        elif lookup_type != 'isnull':
            raise TypeError('Invalid lookup_type: {!r}'.format(lookup_type))
        return super().get_prep_lookup(lookup_type, value)

    def validate(self, value, model_instance):
        return super().validate(self.get_prep_value(value), model_instance)

    def formfield(self, form_class=forms.CharField, **kwargs):
        """Has to be defined as a whole without doing super() because of
        Django bug #9245."""
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            # Fields with choices get special treatment.
            include_blank = self.blank or not (self.has_default() or 'initial' in kwargs)
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.from_python  # XXX: changed
            if self.null:
                defaults['empty_value'] = None
            form_class = _TypedChoiceField  # XXX: changed
            # Many of the subclass-specific formfield arguments (min_value,
            # max_value) don't apply for choice fields, so be sure to only pass
            # the values that TypedChoiceField will understand.
            unneeded = ('coerce', 'empty_value', 'choices', 'required',
                        'widget', 'label', 'initial', 'help_text',
                        'error_messages', 'show_hidden_initial')
            nkwargs = {k: kwargs[k] for k in kwargs if k not in unneeded}
        else:
            nkwargs = kwargs
        defaults.update(nkwargs)
        return form_class(**defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def deconstruct(self):
        # Django 1.7 migrations
        name, path, args, kwargs = super().deconstruct()
        kwargs['choices'] = self.choice_class
        return name, path, args, kwargs


class _TypedChoiceField(forms.TypedChoiceField):
    def clean(self, value):
        return self.coerce(value)

    def prepare_value(self, value):
        return self.coerce(value)
