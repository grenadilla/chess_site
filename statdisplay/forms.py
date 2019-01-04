from django import forms
from statdisplay.models import Player

def get_compare_choices():
    players = Player.objects.all()
    choices = []
    for player in players:
        choices.append((player.user_name, player.user_name))
    return choices

class CompareForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CompareForm, self).__init__(*args, **kwargs)
        self.fields['player1'] = forms.ChoiceField(choices=get_compare_choices())
        self.fields['player2'] = forms.ChoiceField(choices=get_compare_choices())
        self.fields['player1'].widget.attrs['class'] = 'fancy-select'
        self.fields['player2'].widget.attrs['class'] = 'fancy-select'
