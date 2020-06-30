from django import forms
from .models import Notice, Comment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        exclude = ['user']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'image' : '이미지',
            'upload' : '업로드',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['notice', 'user']
        widgets = {
            'content' : forms.TextInput(attrs={'class' : 'form-control' ,'aria-describedby' : 'button-addon2', 'aria-label' : 'comment' })
        }
        labels = {
            'content' : '',
        }

