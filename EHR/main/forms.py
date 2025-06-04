
from  django  import  forms
from  .models import  MedicalRecord

class  MedicalRecordForm(forms.ModelForm):
    class  Meta:
        model =  MedicalRecord
        fields = ['report_file', 'prescription_file', 'medicine_names', 'prescribed_tests']
