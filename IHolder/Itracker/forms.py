from django import forms

class searchForm(forms.Form):
    searchQuery = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(searchForm, self).__init__(*args, **kwargs)
        self.fields['searchQuery'].label = ""
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded'