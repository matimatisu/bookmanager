from django import forms
from .models import Book
from django.utils import timezone
import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title","author","published_date","is_read","read_date","genre"]

        widgets = {
            "publish_date": forms.DateInput(attrs={"type":"date"}),
            "read_date":forms.DateInput(attrs={"type":"date"}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        max_date = today + datetime.timedelta(days=365*2)  # 2年後

        self.fields["published_date"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "max": max_date.strftime("%Y-%m-%d"),
            }
        )