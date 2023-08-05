from django.utils.safestring import mark_safe
import octicons16px

OCTICONS = {}
for key, value in octicons16px.OCTICONS.items():
    OCTICONS[key.replace('-', '_') + '_16px'] = mark_safe(value)

CONTEXT = {'octicons': OCTICONS}


def octicons(request):
    return CONTEXT
