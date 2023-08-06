from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.exceptions import ValidationError
from django.db.models import Model as BaseModel
from django.db.models.deletion import CASCADE
from django.db.models.fields import PositiveIntegerField, TextField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.db.models.query import Q
from django.utils.translation import gettext_lazy as _


def get_default_site_id():
    return Site.objects.get_current().id


class Model(BaseModel):
    """Abstract Model for all models in django_generic_awards package."""

    class Meta:
        abstract = True

    site = ForeignKey(Site, on_delete=CASCADE, default=get_default_site_id, editable=False)
    objects = CurrentSiteManager()


class ImageAttachment(Model):
    """Stores a single image attachment for :code:`object`."""

    class Meta:
        verbose_name = _('image attachment')
        verbose_name_plural = _('image attachments')

    image = ImageField(upload_to='attachments')

    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class AwardManager(CurrentSiteManager):
    """Custom Manager which allows to get only :model:`Awards` suitable for current Object"""

    def prepare_for_form(self, request):
        return


class Award(Model):
    """
    Stores a single Award entry, related to :model:`django_generic_awards.AwardableModel`.

    Each Award have it's Options stored in :model:`django_generic_awards.AwardScoreOption`.

    Field :code:`help_text` is used as Award Options display template: ``{}`` in this template will
    be replaced with actual Award Option's value
    """

    class Meta:
        verbose_name = _('award')
        verbose_name_plural = _('awards')

    name = TextField(_('Name'), null=False, blank=False)
    help_text = TextField(_('Help text'), help_text=_('{} in this string will be replaced with actual Award Score\'s value'), null=False, blank=True)
    award_manager = AwardManager()

    def __str__(self):
        return ' '.join((self.name, self.help_text and self.help_text.format('xx')))


class AwardScoreOption(Model):
    """Stores a score Option for Award, related to :model:`django_generic_awards.Award`."""

    class Meta:
        verbose_name = _('award score option')
        verbose_name_plural = _('award score options')

    award = ForeignKey(Award, on_delete=CASCADE)
    # Binary or external RichTextField for value?
    value = TextField(_('Value'), null=False, blank=False)

    def __str__(self):
        return self.award.help_text and self.award.help_text.format(self.value) or f'{self.award} | {self.value}'


class AwardScoreOptionProxy(AwardScoreOption):
    """Proxy model for :model:`django_generic_awards.AwardScoreOption`."""

    class Meta:
        proxy = True
        verbose_name = _('award score')
        verbose_name_plural = _('award scores')


class ObjectAwardScore(Model):
    """
    Stores a relation from Award Option to any other Object from awardable model,
    related to :model:`django_generic_awards.Award`.

    Object Award Option can be extended for single instance by proving replacement
    Option in :code:`award_score_option_extended`.

    Field :code:`award_addition_info` can be used to provide additinal textual information about
    award context.
    """

    class Meta:
        verbose_name = _('object award score')
        verbose_name_plural = _('object award scores')

    content_type = ForeignKey(ContentType, limit_choices_to=Q(awardablemodels__isnull=False), on_delete=CASCADE)
    object_id = PositiveIntegerField()
    generic_object = GenericForeignKey('content_type', 'object_id')

    award_score_option = ForeignKey(AwardScoreOption, on_delete=CASCADE)
    award_score_option_extended = TextField(_('Extended score'), null=False, blank=True)

    award_addition_info = TextField(_('Additional Information'), null=False, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not AwardableModel.objects.filter(content_type=self.content_type).exists():
            raise ValidationError({'generic_object': 'Should be an Awardable'})
        super().save(force_insert, force_update, using, update_fields)

    def get_score(self):
        return self.award_score_option_extended or self.award_score_option

    def __str__(self):
        return f'{self.award_score_option.award}'


class AwardableModel(Model):
    """Specifies which Model (all of it's Objects) can be awarded with :model:`django_generic_awards.Award`."""

    class Meta:
        verbose_name = _('awardable model')
        verbose_name_plural = _('awardable models')

    content_type = OneToOneField(ContentType, on_delete=CASCADE, related_name='awardablemodels', )
    award_for_concrete_model = ManyToManyField(to=Award, related_name='award_to_model')

    def __str__(self):
        return f'{self._meta.app_label} | {self.content_type.model}'
