from rest_framework.decorators import api_view
from .Action import Action
from .models import department

@api_view(['GET',"POST"]) # 科室列表
def departmentList(request):
  departments = department.objects.all()
  arr = []
  for item in departments:
    temp = {}
    temp['id'] = item.id
    temp['name'] = item.name
    temp['registration_fee'] = item.registration_fee
    arr.append(temp)
  return Action.success(arr)

@api_view(['POST'])
# 添加科室
def departmentAdd(request):
  # 获取参数
  name = request.POST.get('name')
  registration_fee_str = request.POST.get('registration_fee') # 获取挂号费参数

  if not name:
      return Action.fail("科室名称不能为空")
  if not registration_fee_str: # 验证挂号费是否为空
      return Action.fail("挂号费不能为空")

  try:
      registration_fee = float(registration_fee_str) # 尝试转换为浮点数
      if registration_fee < 0:
          return Action.fail("挂号费不能为负数")
  except ValueError:
      return Action.fail("挂号费格式不正确，请输入数字")

  # 查询科室名称是否已被注册
  sameNameDepartment = department.objects.filter(name=name)
  if sameNameDepartment.exists():
    return Action.fail("已存在同名科室")

  # 若没注册，添加入数据库
  new_department = department(name=name, registration_fee=registration_fee) # 保存挂号费
  new_department.save()
  return Action.success("科室添加成功")

@api_view(['POST'])
# 删除科室
def departmentDelete(request):
  department_id = request.POST.get('id')

  if not department_id:
    return Action.fail("缺少科室ID参数")

  try:
    dept = department.objects.get(id=department_id)
    dept_name = dept.name # 记录一下科室名称以便返回提示
    dept.delete()
    return Action.success(f"科室 '{dept_name}' 删除成功")
  except department.DoesNotExist:
    return Action.fail("要删除的科室不存在")
  except Exception as e:
    return Action.fail(f"删除失败: {str(e)}")
