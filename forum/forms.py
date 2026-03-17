from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'genre', 'file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Beethoven Sonata Op. 27 No. 2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the piece, difficulty level, instrumentation...'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'file': 'Sheet Music File (PDF or image)',
            'thumbnail': 'Cover Image (optional)',
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed = ['.pdf', '.png', '.jpg', '.jpeg', '.gif']
            ext = '.' + file.name.rsplit('.', 1)[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError('Only PDF and image files are allowed.')
            if file.size > 20 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 20MB.')
        return file


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Leave a comment...',
            }),
        }
        labels = {'body': ''}
