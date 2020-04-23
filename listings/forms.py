from django import forms
from django.forms import ModelForm
from .models import Listing, Category, ListingRating, ListingComment
from taggit.forms import TagWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class AddListingForm(ModelForm):
    FACILITY_STATUS_CHOICES = (
        ('0', 'No'),
        ('1', 'Yes'),
    )

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'gallery-photo-add'}), label='Images For Listing  ')
    facility_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Facility Name'}), required=True)
    facility_status_choice = forms.ChoiceField(
        choices=FACILITY_STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Listing
        exclude = ['owner', 'active', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price'}),
            'area': forms.TextInput(attrs={'placeholder': 'Area/Location'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput', 'class': 'w-100'}),
            'start_time': DateInput(),
            'end_time': DateInput()
        }

    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 5:
            raise forms.ValidationError(
                "You Can Not Upload More Than 4 Images")
        return images

    def clean_city(self):
        return self.cleaned_data.get('city').title()

    def clean_area(self):
        return self.cleaned_data.get('area').title()

    def __init__(self, *args, **kwargs):
        # call the parent init
        super(AddListingForm, self).__init__(*args, **kwargs)
        # change the widget to use checkboxes
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.all())

        self.fields['facility_name'].label = ''


class EditListingForm(ModelForm):
    FACILITY_STATUS_CHOICES = (
        ('0', 'No'),
        ('1', 'Yes'),
    )

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'gallery-photo-add'}), label='Images For Listing  ', required=False)
    facility_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Facility Name'}), required=False)
    facility_status_choice = forms.ChoiceField(
        choices=FACILITY_STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=False)

    class Meta:
        model = Listing
        exclude = ['owner', 'active', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price'}),
            'area': forms.TextInput(attrs={'placeholder': 'Area/Location'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            'tags': TagWidget(),
            'start_time': DateInput(),
            'end_time': DateInput()
        }

    def clean_city(self):
        return self.cleaned_data.get('city').title()

    def clean_area(self):
        return self.cleaned_data.get('area').title()

    def __init__(self, *args, **kwargs):
        # call the parent init
        super(EditListingForm, self).__init__(*args, **kwargs)
        self.fields['facility_name'].label = ''


class ListingRatingForm(ModelForm):
    rating = forms.FloatField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1'}), min_value=0.0, max_value=10.0)
    facility = forms.FloatField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1'}), min_value=0.0, max_value=10.0)
    staff = forms.FloatField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1'}), min_value=0.0, max_value=10.0)
    price = forms.FloatField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1'}), min_value=0.0, max_value=10.0)

    class Meta:
        model = ListingRating
        exclude = ['listing', 'user', 'average_rating']


class ListingCommentForm(ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = ListingComment
        exclude = ['listing', 'user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = self.request.user
        super(ListingCommentForm, self).__init__(*args, **kwargs)

        if user.is_authenticated:
            self.fields['name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email

            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['readonly'] = True
