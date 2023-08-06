from urllib.parse import urlparse

from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import TextField
from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from django.urls import resolve

from django_generic_awards.actions import AddAward
from django_generic_awards.forms.fields import SVGAndImageFormField
from django_generic_awards.mixins import DisableAddRelatedMixin
from django_generic_awards.models import (
    Award, AwardableModel, AwardScoreOption, ObjectAwardScore, ImageAttachment,
    AwardScoreOptionProxy)


class ObjectAwardScoreInlineForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = ObjectAwardScore


class ObjectAwardScoreInline(GenericTabularInline):
    model = ObjectAwardScore
    form = ObjectAwardScoreInlineForm
    extra = 0

    search_fields = ['value']
    autocomplete_fields = ('award_score_option',)
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1})},
    }

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['award_score_option'].widget.can_add_related = False
        formset.form.base_fields['award_score_option'].widget.can_change_related = False
        return formset


class ImageAttachmentForm(ModelForm):
    class Meta:
        model = ImageAttachment
        fields = ['image']
        field_classes = {
            'image': SVGAndImageFormField,
        }


class ImageAttachmentInline(GenericTabularInline):
    form = ImageAttachmentForm
    model = ImageAttachment
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1})},
    }


class GenericAwardsAdminMixin(BaseModelAdmin):
    mixin_inlines = (ImageAttachmentInline,)
    conditional_inlines = (ObjectAwardScoreInline,)

    @property
    def is_model_awardable(self):
        model_content_type = ContentType.objects.get_for_model(self.model)
        return AwardableModel.objects.filter(content_type=model_content_type).exists()

    def get_inlines(self, request, obj=None):
        inlines = super().get_inlines(request, obj)
        new_inlines = list(inlines) + list(self.mixin_inlines)

        if self.is_model_awardable:
            new_inlines += self.conditional_inlines
        return sorted(set(new_inlines), key=lambda i: str(type(i)))

    def get_actions(self, request):
        updater = {}
        if self.is_model_awardable:
            updater[AddAward.name] = (AddAward.as_view(), AddAward.name, AddAward.short_description)
        return dict(super().get_actions(request), **updater)


class ModelAdmin(BaseModelAdmin):
    inlines = (ImageAttachmentInline,)


class AwardScoreOptionInline(TabularInline):
    model = AwardScoreOptionProxy
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1})},
    }


@admin.register(Award)
class AwardAdmin(ModelAdmin):
    inlines = (AwardScoreOptionInline,)


@admin.register(AwardScoreOption)
class AwardScoreOptionAdmin(ModelAdmin):
    search_fields = ['value', 'award__name', 'award__help_text']

    def get_search_results(self, request, queryset, search_term):
        referer = request.META['HTTP_REFERER']
        resolved = resolve(urlparse(referer).path)
        object_id = resolved.kwargs.get('object_id')
        if object_id:
            model_admin = resolved.func.model_admin
            model_content_type = ContentType.objects.get_for_model(model_admin.model)
            awards = AwardableModel.objects.get(content_type=model_content_type.id).award_for_concrete_model.all()
            queryset = AwardScoreOption.objects.filter(award__in=awards)

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


@admin.register(ObjectAwardScore)
class ObjectAwardScoreAdmin(ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(AwardableModel)
class AwardableModelAdmin(DisableAddRelatedMixin, ModelAdmin):
    filter_horizontal = ['award_for_concrete_model']
    disable_add_related = ['award_for_concrete_model']
