from django import forms
class inp(forms.Form):
    g_1=forms.DecimalField(label='Effective Green Time (P1)')
    g_2=forms.DecimalField(label='Effective Green Time (P2)')
    g_3=forms.DecimalField(label='Effective Green Time (P3)')
    g_4=forms.DecimalField(label='Effective Green Time (P4)')
    t=forms.DecimalField(label='Time (sec)')
#g,t
