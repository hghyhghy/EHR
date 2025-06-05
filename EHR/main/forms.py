
from  django  import  forms
from  .models import  MedicalRecord

class  MedicalRecordForm(forms.ModelForm):
    class  Meta:
        model =  MedicalRecord
        fields = ['report_file', 'prescription_file', 'medicines_name', 'prescribed_tests']
