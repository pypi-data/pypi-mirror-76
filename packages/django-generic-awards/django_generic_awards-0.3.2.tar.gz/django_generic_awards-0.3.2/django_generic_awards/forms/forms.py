from django.forms import Form
from django.forms.fields import ChoiceField, MultipleHiddenInput
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.utils.translation import gettext_lazy as _

ACTION_ANSWERS = (
    ('add_to_all', _('Add selected Awards to all objects')),
    ('clear_from_all', _('Clear selected Awards from all object')),
)

INITIAL_ACTION_ANSWER = 'add_to_all'


class AddAwardForm(Form):
    objects = ModelMultipleChoiceField(queryset=None, widget=MultipleHiddenInput())
    awards = ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=None)
    action_answer = ChoiceField(choices=ACTION_ANSWERS, initial=INITIAL_ACTION_ANSWER, widget=RadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        objects = kwargs.pop('objects', [])
        awards = kwargs.pop('awards', [])

        self.base_fields.get('objects').queryset = objects
        self.base_fields.get('awards').queryset = awards

        super().__init__(*args, **kwargs)


FORM_ANSWERS = (
    ('yes', _('Yes, I’m sure')),
    ('no', _('No, take me back')),
)

POSITIVE_FORM_ANSWER = 'yes'


class AddAwardAnswerForm(Form):
    answer = ChoiceField(choices=FORM_ANSWERS, required=True)

    @property
    def is_positive(self):
        return self.cleaned_data['answer'] == POSITIVE_FORM_ANSWER
