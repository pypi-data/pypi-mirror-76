from django import forms
from django.forms import Media
from django.utils.functional import cached_property
from wagtail.admin.rich_text import DraftailRichTextArea


class NonAdminDraftailRichTextArea(forms.TextInput, DraftailRichTextArea):
    template_name = 'non_admin_draftail/widgets/non_admin_draftail_rich_text_area.html'

    @cached_property
    def media(self):
        media = Media(js=[
            'non_admin_draftail/draftail/draftail.js',
        ], css={
            'all': [
                # CSS from Draftail bundle
                'non_admin_draftail/draftail/draftail.css',
                # CSS from Wagtail admin (black toolbar theme)
                'wagtailadmin/css/panels/draftail.css',
                # Wagtail font (for toolbar icons)
                'non_admin_draftail/fonts/wagtail-font.css'
            ]
        })

        for plugin in self.plugins:
            media += plugin.media

        return media

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'non-admin-draftail__hidden-input'
        return context
