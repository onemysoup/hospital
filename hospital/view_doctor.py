from rest_framework.decorators import api_view
from .Action import Action
from .models import user_doctor, department
from .serializers import UserDoctorSerializer


@api_view(['GET',"POST"])
# 医生登录
def doctorLogin(request):
  # 获取参数
  id_card = request.POST.get('id_card') or request.POST.get('name')
  password = request.POST.get('password')
  # 根据身份证查询
  user = user_doctor.objects.filter(id_card=id_card).first()
  if not user:
    # 用户不存在,则直接返回错误消息
    return Action.fail("用户不存在")
  if user.password != password:
    # 用户存在,密码不一致,则直接返回错误消息
    return Action.fail("密码错误")
  # 登陆成功
  return Action.success(UserDoctorSerializer(user, many = False).data)

@api_view(['GET',"POST"])
# 医生列表
def doctorList(request):
  doctors = user_doctor.objects.all()
  arr = []
  for item in doctors:
    temp = {}
    temp['id'] = item.id
    temp['name'] = item.name
    temp['id_card'] = item.id_card
    temp['department_id'] = item.department_id
    temp['department_name'] = department.objects.filter(id=item.department_id).first().name
    temp['shift_status'] = item.shift_status if hasattr(item,'shift_status') and item.shift_status is not None else '未知状态'
    # temp['password'] = item.password
    # temp['status'] = item.status
    arr.append(temp)
  # 登陆成功
  return Action.success(arr)

@api_view(['GET',"POST"])
# 添加医生
def doctorAdd(request):
  # 获取参数
  name = request.POST.get('name')
  id_card = request.POST.get('id_card')
  department_id = request.POST.get('department_id')
  password = request.POST.get('password')
  # 查询身份证号是否已被注册
  sameIdCardUserList = user_doctor.objects.filter(id_card=id_card)
  if sameIdCardUserList.exists() == True :
    # 如果已经被注册,则直接返回错误消息
    return Action.fail("身份重复")
  # 若没注册，添加入数据库
  doctor = user_doctor(name=name, id_card=id_card, department_id=department_id, password=password)
  doctor.save()
  # 添加成功
  return Action.success()

@api_view(['POST'])
# 删除医生
def doctorDelete(request):
  # 获取要删除的医生ID
  doctor_id = request.POST.get('id')

  if not doctor_id:
    return Action.fail("缺少医生ID参数")

  try:
    # 尝试获取医生对象
    doc = user_doctor.objects.get(id=doctor_id)
    doc_name = doc.name # 获取医生姓名以便在成功消息中使用
    doc.delete() # 删除医生
    return Action.success(f"医生 '{doc_name}' 删除成功")
  except user_doctor.DoesNotExist:
    # 如果医生不存在
    return Action.fail("要删除的医生不存在")
  except Exception as e:
    # 捕获其他可能的异常
    return Action.fail(f"删除失败: {str(e)}")


@api_view(['POST'])
def doctorEditShiftStatus(request):
  doctor_id = request.POST.get('id')
  shift_status = request.POST.get('shift_status')  # 接收新的值班状态

  if not doctor_id or not shift_status:
    return Action.fail("缺少医生ID或值班状态参数")

  try:
    doctor_obj = user_doctor.objects.get(id=doctor_id)
    doctor_obj.shift_status = shift_status
    doctor_obj.save()
    return Action.success("医生值班状态修改成功")
  except user_doctor.DoesNotExist:
    return Action.fail("医生不存在")
  except Exception as e:
    return Action.fail(f"修改值班状态失败: {str(e)}")

@api_view(['GET', 'POST'])
def getMyDoctorInfo(request):
  doctor_id = request.POST.get('id')  # 假设前端会传递当前登录医生的ID

  if not doctor_id:
    return Action.fail("缺少医生ID参数")

  try:
    doctor_obj = user_doctor.objects.get(id=doctor_id)
    # 使用 UserDoctorSerializer 序列化数据
    serialized_data = UserDoctorSerializer(doctor_obj).data
    return Action.success(serialized_data)
  except user_doctor.DoesNotExist:
    return Action.fail("医生不存在")
  except Exception as e:
    return Action.fail(f"获取医生信息失败: {str(e)}")