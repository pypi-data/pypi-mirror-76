import uuid

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

JQUERY_JS = "admin/js/vendor/jquery/jquery.js"
JQUERY_INIT_JS = "admin/js/jquery.init.js"

def jquery_plugins(jslist):
    return [JQUERY_JS] + jslist + [JQUERY_INIT_JS]


class UuidFieldSearchableAdmin(admin.ModelAdmin):
    """Enable search by uuid string with dashes.
    """
    def get_search_results(self, request, queryset, search_term):
        try:
            search_term_new = search_term
            if isinstance(search_term_new, str):
                search_term_new = search_term_new.strip()
            search_term_new = uuid.UUID(search_term_new).hex
        except ValueError:
            search_term_new = search_term
        result = super().get_search_results(request, queryset, search_term_new)
        return result



class InlineBooleanFieldsAllowOnlyOneCheckedMixin(InlineModelAdmin):
    """Admin inline formset has a boolean field, so that there are many checkboxes of that field, make sure that only one checkbox is checked.
    """

    special_class_name = "inline-boolean-fields-allow-only-one-checked"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "django-jquery-plugins/jquery.utils.js",
            "django-jquery-plugins/inline-boolean-fields-allow-only-one-checked.js",
        ])
