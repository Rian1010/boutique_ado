from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
# import gettext_lazy as _ means that "_" can be used as an alias of "gettext_lazy"


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'