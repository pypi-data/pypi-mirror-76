from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import info
from django.forms.models import modelform_factory
from django.utils.decorators import classonlymethod
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from django_generic_awards.forms.forms import AddAwardAnswerForm, AddAwardForm
from django_generic_awards.models import ObjectAwardScore, AwardScoreOption


class ActionView(FormView):
    allow_empty = False
    name = ''
    short_description = ''
    description = ''
    counter = 0
    cancel_message = _(u'Action cancelled')
    finished_message = ''

    @cached_property
    def answer(self):
        return AddAwardAnswerForm(**super(ActionView, self).get_form_kwargs())

    @classonlymethod
    def as_view(cls, **initkwargs):
        response = super(ActionView, cls).as_view(**initkwargs)
        response.short_description = cls.short_description
        response.allow_empty = cls.allow_empty
        return response

    def get_queryset(self, **kwargs):
        return getattr(self, 'queryset', [])

    def get_object(self):
        for obj in self.get_queryset():
            return obj

    def get_form(self, form_class=None, **kwargs):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ActionView, self).get_form(form_class)
        if hasattr(form, 'prepare'):
            return form.prepare(request=self.request, **dict({'prefix': self.get_prefix()}, **kwargs))
        form.request = self.request
        return form

    def dispatch(self, admin, request, queryset, *args, **kwargs):
        self.request = request
        self.admin = admin
        self.model = admin.model
        self.queryset = queryset
        return super(ActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.answer.is_valid():
            if self.answer.is_positive:
                return self.processing(*args, **kwargs)
            return self.finished(cancel=True)
        return self.get(request, *args, **kwargs)

    def processing(self, *args, **kwargs):
        return self.finished(*args, **kwargs)

    def finished(self, cancel=False, **kwargs):
        message = cancel and self.cancel_message or self.finished_message
        action = kwargs.pop('action', '')

        if not cancel:
            message = message.format(**dict(
                counter=self.counter,
                action=action
            ))
        info(self.request, message)

    def get(self, request, *args, **kwargs):
        if self.get_form_class():
            self.request.method = 'GET'
            return super(ActionView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = {
            'title': '%s. %s' % (self.short_description, _('Are you sure?')),
            'action_short_description': self.short_description,
            'action_name': self.name,
            'objects_name': str(self.model._meta.verbose_name_plural),
            'action_objects': self.get_queryset(),
            'queryset': self.get_queryset(),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'form': self.get_form(),
            'answer_form': self.answer,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        }
        context.update(kwargs)
        return context

    def log(self, obj, action_flag=CHANGE, **kwargs):
        content_type = ContentType.objects.get_for_model(obj)
        object_repr = str(obj)
        LogEntry(
            user=self.request.user,
            content_type=content_type,
            object_id=obj.pk,
            object_repr=object_repr,
            action_flag=action_flag,
            **kwargs
        ).save()


class AddAward(ActionView):
    form_class = AddAwardForm
    name = 'add_award'
    short_description = _('Add/clear awards')
    template_name = 'admin/award_confirmation.html'
    finished_message = _('{counter} awards have been {action}')
    action_cleared = _('cleared')
    action_added = _('added')

    def get_model(self):
        return getattr(self.get_queryset(), 'model', None)

    def get_form_kwargs(self):
        objects = self.get_queryset()
        object_ids = objects.values_list('pk', flat=True)
        content_type = ContentType.objects.get_for_model(objects.model)

        awards_ids = ObjectAwardScore.objects.filter(
            content_type=content_type, object_id__in=object_ids
        ).values_list('award_score_option_id', flat=True)
        awards = AwardScoreOption.objects.filter(pk__in=awards_ids)

        kwargs = {
            'objects': objects,
            'awards': awards,
            'initial': {
                'objects': objects.values_list('pk', flat=True),
                'awards': awards.values_list('pk', flat=True),
            }
        }
        return dict(super(AddAward, self).get_form_kwargs(), **kwargs)

    def get_form_class(self):
        return modelform_factory(self.get_model(), fields='__all__', form=super(AddAward, self).get_form_class())

    def get_context_data(self, **kwargs):
        context = {
            'objects': self.queryset
        }
        return dict(super(AddAward, self).get_context_data(**kwargs), **context)

    def processing(self, *args, **kwargs):
        awards_ids = self.request.POST.getlist('awards')
        objects_ids = self.request.POST.getlist('objects')
        action_answer = self.request.POST.get('action_answer')

        awards = AwardScoreOption.objects.filter(pk__in=awards_ids)
        model = self.request.resolver_match.func.model_admin.model
        content_type = ContentType.objects.get_for_model(model)

        action = ''
        if action_answer == 'clear_from_all':
            action = self.action_cleared
            marked_for_deletion = ObjectAwardScore.objects.filter(
                content_type=content_type,
                object_id__in=objects_ids,
                award_score_option__in=awards
            )
            for obj in marked_for_deletion:
                self.log(obj, action_flag=DELETION)
            self.counter, _ = marked_for_deletion.delete()
        elif action_answer == 'add_to_all':
            action = self.action_added
            pass
        return super(AddAward, self).processing(*args, action=action, **kwargs)
