from django import forms
class inp(forms.Form):
    C=forms.DecimalField(label='Cycle Length (sec)')
    g_c=forms.DecimalField(label='Effective Green Ratio')
    t=forms.DecimalField(label='Time (sec)')
