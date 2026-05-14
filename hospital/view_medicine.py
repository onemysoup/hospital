from rest_framework.decorators import api_view
from .Action import Action
from .models import medicine
from .serializers import MedicineSerializer

@api_view(['GET',"POST"])
# 药品列表
def medicineList(request):
  medicines = medicine.objects.all()
  return Action.success(MedicineSerializer(medicines, many = True).data)

@api_view(['GET',"POST"])
# 药品列表
def medicineStrList(request):
  medicine_list = request.POST.get('medicine_list', '')
  if not medicine_list:
    return Action.success([])
  medicine_list_arr = medicine_list.split(',')
  arr = []
  for de in medicine_list_arr:
    med = medicine.objects.filter(id=de).first()
    if not med:
      continue
    temp = {}
    temp['id'] = med.id
    temp['name'] = med.name
    temp['price'] = med.price
    temp['unit'] = med.unit
    temp['quantity'] = med.quantity
    arr.append(temp)
  return Action.success(arr)

@api_view(['GET',"POST"])
# 添加药品
def medicineAdd(request):
  # 获取参数
  name = request.POST.get('name')
  price = request.POST.get('price')
  unit = request.POST.get('unit')
  quantity = request.POST.get('quantity')
  # 查询
  sameIdCardUserList = medicine.objects.filter(name=name)
  if sameIdCardUserList.exists() == True :
    # 如果已经被注册,则直接返回错误消息
    return Action.fail("已存在")
  # 若没注册，添加入数据库
  new_medicine = medicine(name=name, price=price, unit=unit, quantity=quantity or 0)
  new_medicine.save()
  # 添加成功
  return Action.success("药品添加成功")

@api_view(['POST'])
# 删除药品
def medicineDelete(request):
  medicine_id = request.POST.get('id')

  if not medicine_id:
    return Action.fail("缺少药品ID参数")

  try:
    med = medicine.objects.get(id=medicine_id)
    med_name = med.name # 记录一下药品名称以便返回提示
    med.delete()
    return Action.success(f"药品 '{med_name}' 删除成功")
  except medicine.DoesNotExist:
    return Action.fail("要删除的药品不存在")
  except Exception as e:
    return Action.fail(f"删除失败: {str(e)}")

#修改药品信息
@api_view(['POST'])
def medicineEdit(request):
    medicine_id = request.POST.get('id')
    name = request.POST.get('name')
    price = request.POST.get('price')
    unit = request.POST.get('unit')
    quantity = request.POST.get('quantity') # 获取 quantity 参数

    if not medicine_id:
        return Action.fail("缺少药品ID参数")

    try:
        med = medicine.objects.get(id=medicine_id)
        # 检查除当前药品外是否有其他药品使用相同名称
        if name and medicine.objects.filter(name=name).exclude(id=medicine_id).exists():
            return Action.fail("药品名称已存在")

        if name: # 如果名称有提供，则更新
            med.name = name
        if price: # 如果价格有提供，则更新
            med.price = price
        if unit: # 如果单位有提供，则更新
            med.unit = unit
        if quantity is not None:
            med.quantity = int(quantity) # 确保转换为整数

        med.save()
        return Action.success("药品信息修改成功")
    except medicine.DoesNotExist:
        return Action.fail("药品不存在")
    except Exception as e:
        return Action.fail(f"修改失败: {str(e)}")