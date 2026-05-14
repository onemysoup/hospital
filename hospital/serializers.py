import logging

from rest_framework import serializers
from .models import admin, user_patient, user_doctor, department, medicine, order


logger = logging.getLogger(__name__)


# 对数据进行序列化
# 患者数据序列化
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = admin
        fields = ['id', 'name', 'password']

# 患者数据序列化
class UserPatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_patient
        fields = ['id', 'name', 'id_card', 'phone', 'password', 'sex', 'age']

# 医生数据序列化
class UserDoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_doctor
        fields = ['id', 'name', 'id_card', 'department_id', 'password', 'status', 'shift_status', 'department_name']

    department_name = serializers.SerializerMethodField()
    def get_department_name(self, obj):
        try:
            department_obj = department.objects.filter(id=obj.department_id).first()
            if department_obj:
                return department_obj.name
            else:
                return "未知科室"
        except Exception as e:
            logger.exception("Error in get_department_name for doctor ID %s: %s", obj.id, e)
            return "未知科室"

# 科室数据序列化
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = department
        fields = ['id', 'name', 'registration_fee', 'doctor_num']

# 药品数据序列化
class MedicineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = medicine
        fields = ['id', 'name', 'price', 'unit','quantity']

# 挂号
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = order
        fields = ['id', 'patient_id', 'department_id', 'readme', 'registration_fee', 'doctor_id', 'order_advice', 'medicine_list', 'total_cost', 'status', 'time']
