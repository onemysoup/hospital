from hospital import view_admin
from hospital import view_patient
from hospital import view_doctor
from hospital import view_medicine
from hospital import view_department
from hospital import view_order
from django.urls import path
from . import views

urlpatterns = [
    #页面请求
    path('login/', views.login),
    path('admin/', views.admin_department),
    path('admin_department/', views.admin_department),
    path('admin_doctor/', views.admin_doctor),
    path('admin_medicine/', views.admin_medicine),
    path('admin_patient/', views.admin_patient),

    path('patient/', views.patient_home),
    path('patient_home/', views.patient_home),
    path('patient_order/', views.patient_order),

    path('doctor/', views.doctor_order),
    path('doctor_home/', views.doctor_home),
    path('doctor_order/', views.doctor_order),

    #数据请求

    #管理员
    path('adminLogin', view_admin.adminLogin, name='adminLogin'),
    path('departmentList', view_department.departmentList, name='departmentList'),
    path('departmentAdd', view_department.departmentAdd, name='departmentAdd'),
    path('departmentDelete', view_department.departmentDelete, name='departmentDelete'),
    path('doctorList', view_doctor.doctorList, name='doctorList'),
    path('doctorAdd', view_doctor.doctorAdd, name='doctorAdd'),
    path('doctorDelete', view_doctor.doctorDelete, name='doctorDelete'),
    path('doctorEditShiftStatus', view_doctor.doctorEditShiftStatus, name='doctorEditShiftStatus'), # <-- 新增行
    path('getMyDoctorInfo', view_doctor.getMyDoctorInfo, name='getMyDoctorInfo'),
    path('patientList', view_patient.patientList, name='patientList'),
    path('patientAdd', view_patient.patientRegister, name='patientAdd'),
    # 药品
    path('medicineList', view_medicine.medicineList, name='medicineList'),
    path('medicineStrList', view_medicine.medicineStrList, name='medicineStrList'),
    path('medicineAdd', view_medicine.medicineAdd, name='medicineAdd'),
    path('medicineDelete', view_medicine.medicineDelete, name='medicineDelete'),
    path('medicineEdit', view_medicine.medicineEdit, name='medicineEdit'),
    #患者
    path('patientRegister', view_patient.patientRegister, name='patientRegister'),
    path('patientLogin', view_patient.patientLogin, name='patientLogin'),
    # 就诊
    path('orderAdd', view_order.orderAdd, name='orderAdd'),
    path('orderList', view_order.orderList, name='orderList'),
    path('orderInfo', view_order.orderInfo, name='orderInfo'),
    path('orderTakeNumber', view_order.orderTakeNumber, name='orderTakeNumber'),
    path('orderFinish', view_order.orderFinish, name='orderFinish'),
    path('orderPay', view_order.orderPay, name='orderPay'), # 新增的缴费API

    #医生
    path('doctorLogin', view_doctor.doctorLogin, name='doctorLogin'),
]
