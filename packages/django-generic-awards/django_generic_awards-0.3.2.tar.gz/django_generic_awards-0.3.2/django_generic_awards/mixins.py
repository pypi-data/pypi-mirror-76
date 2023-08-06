class DisableAddRelatedMixin:
    """
    Remove plus sign for related fields specified in `disable_add_related` list
    Check https://code.djangoproject.com/ticket/9071
    """

    disable_add_related = []

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field_name in self.disable_add_related:
            field = form.base_fields.get(field_name)
            if field:
                field.widget.can_add_related = False
        return form
