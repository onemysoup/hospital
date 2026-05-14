from django.db import transaction
import logging
from rest_framework.decorators import api_view
from .Action import Action
from .models import order, user_patient, department, user_doctor, medicine
from decimal import Decimal  # 导入 Decimal 用于精确计算
from django.db.models import F  # 导入 F 对象用于原子性更新


logger = logging.getLogger(__name__)


@api_view(['GET', "POST"])
# 挂号列表
def orderList(request):
    user_id = request.POST.get('user_id')
    department_id = request.POST.get('department_id')
    doctor_id = request.POST.get('doctor_id')
    status = request.POST.get('status')

    orders_queryset = order.objects.all()

    if user_id:
        orders_queryset = orders_queryset.filter(patient_id=user_id)
    if department_id:
        orders_queryset = orders_queryset.filter(department_id=department_id)
    if doctor_id:
        orders_queryset = orders_queryset.filter(doctor_id=doctor_id)
    if status:
        orders_queryset = orders_queryset.filter(status=status)

    arr = []
    for item in orders_queryset:
        temp = {}
        temp['id'] = item.id
        temp['patient_id'] = item.patient_id  # 直接返回ID

        # 手动查询 patient_name，并处理可能为None的情况
        patient_obj = user_patient.objects.filter(id=item.patient_id).first()
        temp['patient_name'] = patient_obj.name if patient_obj else 'N/A'

        temp['department_id'] = item.department_id  # 直接返回ID
        # 手动查询 department_name
        department_obj = department.objects.filter(id=item.department_id).first()
        temp['department_name'] = department_obj.name if department_obj else 'N/A'

        temp['readme'] = item.readme
        # 在转换为float之前检查是否为None
        temp['registration_fee'] = float(item.registration_fee) if item.registration_fee is not None else 0.0

        temp['doctor_id'] = item.doctor_id  # 直接返回ID
        # 手动查询 doctor_name
        doctor_obj = user_doctor.objects.filter(id=item.doctor_id).first()
        temp['doctor_name'] = doctor_obj.name if doctor_obj else ''

        temp['order_advice'] = item.order_advice
        temp['medicine_list'] = item.medicine_list
        # 在转换为float之前检查是否为None
        temp['total_cost'] = float(item.total_cost) if item.total_cost is not None else 0.0

        # 确保返回给前端的键名与前端期望的 prop 属性一致
        # 并在为None或空字符串时提供默认值
        temp['payment_status'] = item.payment_status if item.payment_status else '未知状态'

        # 将后端字段名 `numbertake_status` 映射给前端期望的 `number_take_status`
        temp['number_take_status'] = item.numbertake_status if item.numbertake_status else '未知状态'

        temp['status'] = item.status
        temp['time'] = item.time.strftime('%Y-%m-%d %H:%M:%S') if item.time else None  # 格式化时间

        arr.append(temp)
    return Action.success(arr)


@api_view(['GET', "POST"])
# 添加就诊
def orderAdd(request):
    # 获取参数
    user_id = request.POST.get('user_id')
    department_id = request.POST.get('department_id')
    readme = request.POST.get('readme')

    # 查询
    checkOrder = order.objects.filter(patient_id=user_id, department_id=department_id, status=1).first()
    if checkOrder:
        return Action.fail("请勿重复挂号")

    checkDepartment = department.objects.filter(id=department_id).first()
    if not checkDepartment:
        return Action.fail("科室不存在")

    checkPatient = user_patient.objects.filter(id=user_id).first()
    if not checkPatient:
        return Action.fail("病人不存在")

    # 若没注册，添加入数据库
    newOrder = order(
        patient_id=user_id,
        department_id=department_id,
        readme=readme,
        registration_fee=checkDepartment.registration_fee,
        doctor_id=0,
        order_advice='',
        medicine_list='',
        total_cost=checkDepartment.registration_fee,
        status=1,
        payment_status='未缴费',
        numbertake_status='未取号'
    )
    newOrder.save()
    return Action.success("挂号成功")  # 增加成功消息


@api_view(['GET', "POST"])
# 就诊详情
def orderInfo(request):
    # 获取参数
    id = request.POST.get('id')
    # 查询
    checkOrder = order.objects.filter(id=id).first()
    if not checkOrder:
        return Action.fail("订单不存在")

    temp = {}
    temp['id'] = checkOrder.id
    temp['patient_id'] = checkOrder.patient_id
    patient_obj = user_patient.objects.filter(id=checkOrder.patient_id).first()
    temp['patient_name'] = patient_obj.name if patient_obj else 'N/A'

    temp['department_id'] = checkOrder.department_id
    department_obj = department.objects.filter(id=checkOrder.department_id).first()
    temp['department_name'] = department_obj.name if department_obj else 'N/A'

    temp['readme'] = checkOrder.readme
    temp['registration_fee'] = float(checkOrder.registration_fee) if checkOrder.registration_fee is not None else 0.0

    temp['doctor_id'] = checkOrder.doctor_id
    doctor_obj = user_doctor.objects.filter(id=checkOrder.doctor_id).first()
    temp['doctor_name'] = doctor_obj.name if doctor_obj else ''  # 确保即使没有医生也能正常显示

    temp['order_advice'] = checkOrder.order_advice
    # **修正：在转换为float之前检查是否为None**
    temp['total_cost'] = float(checkOrder.total_cost) if checkOrder.total_cost is not None else 0.0

    temp['payment_status'] = checkOrder.payment_status if checkOrder.payment_status else '未知状态'
    temp['number_take_status'] = checkOrder.numbertake_status if checkOrder.numbertake_status else '未知状态'
    temp['status'] = checkOrder.status
    temp['time'] = checkOrder.time.strftime('%Y-%m-%d %H:%M:%S') if checkOrder.time else None
    return Action.success(temp)


@api_view(['GET', "POST"])
# 完成就诊
def orderFinish(request):
    # 获取参数
    id = request.POST.get('id')
    order_advice = request.POST.get('order_advice')
    medicine_list = request.POST.get('medicine_list')
    doctor_id = request.POST.get('doctor_id')

    checkOrder = order.objects.filter(id=id).first()
    if not checkOrder:
        return Action.fail("订单不存在")

    if checkOrder.status != 1:  #  1 是“待就诊”状态
        return Action.fail("该病人已处理或状态不正确")

    # 确保从 DecimalField 读取的值转换为 Decimal，再进行计算
    cost_sum = Decimal(str(checkOrder.registration_fee)) if checkOrder.registration_fee is not None else Decimal('0.00')

    if medicine_list:  # 检查 medicine_list 是否为空
        medicine_ids = medicine_list.split(',')
        for med_id_str in medicine_ids:
            try:
                med_id = int(med_id_str)
                med = medicine.objects.filter(id=med_id).first()
                if med:
                    # 确保从 DecimalField 读取的值转换为 Decimal，再进行计算
                    cost_sum += Decimal(str(med.price)) if med.price is not None else Decimal('0.00')
                else:
                    logger.warning("Medicine with ID %s not found when calculating cost.", med_id)
            except ValueError:
                logger.warning("Invalid medicine ID in list: %s", med_id_str)
            except Exception as e:
                logger.exception("Error processing medicine ID %s for cost calculation: %s", med_id_str, e)

    # 直接赋值 SmallIntegerField
    checkOrder.doctor_id = doctor_id

    checkOrder.order_advice = order_advice
    checkOrder.medicine_list = medicine_list  # 存储逗号分隔的药品ID字符串
    checkOrder.status = 2  #  2 是“问诊完成”状态
    checkOrder.total_cost = cost_sum  # 保存 Decimal 类型

    # 将缴费状态重置为“未缴费”
    checkOrder.payment_status = '未缴费'

    checkOrder.save()
    return Action.success("就诊完成，费用已计算，待患者二次缴费")  # 增加成功消息


@api_view(['POST'])
# 缴费功能
def orderPay(request):
    order_id = request.POST.get('id')

    if not order_id:
        logger.warning("Missing order_id when paying order")
        return Action.fail("缺少订单ID参数")

    try:
        with transaction.atomic():  # 使用事务确保操作的原子性
            # 使用 select_for_update 锁定订单行，防止并发问题
            ord_obj = order.objects.select_for_update().get(id=order_id)
            logger.info("Processing payment for order %s, current status: %s", ord_obj.id, ord_obj.payment_status)

            if ord_obj.payment_status == '已缴费':
                return Action.fail(f"订单 '{ord_obj.id}' 已是已缴费状态，无需重复缴费。")

            if ord_obj.medicine_list:
                medicine_ids_str_list = ord_obj.medicine_list.split(',')

                # 遍历药品ID并进行库存扣减
                for med_id_str in medicine_ids_str_list:
                    try:
                        med_id = int(med_id_str.strip())  # 确保去除空白符
                    except ValueError:
                        logger.warning("Invalid medicine ID '%s' in order %s, skipping.", med_id_str, ord_obj.id)
                        continue

                    try:
                        med_obj = medicine.objects.select_for_update().get(id=med_id)

                        if med_obj.quantity >= 1:  # 确保库存足够扣减至少1个
                            medicine.objects.filter(id=med_id).update(quantity=F('quantity') - 1)
                        else:
                            # 如果库存不足，通常会回滚整个事务并返回失败
                            raise ValueError(f"药品 '{med_obj.name}' (ID: {med_obj.id}) 库存不足，无法完成缴费。")
                    except ValueError:
                        raise
                    except medicine.DoesNotExist:
                        logger.warning("Medicine ID %s in order %s does not exist, skipping.", med_id_str, ord_obj.id)
                    except Exception as e:
                        logger.exception("Unexpected error reducing stock for medicine ID %s: %s", med_id_str, e)
                        raise  # 重新抛出异常，让外层事务捕获并回滚

            # 将缴费状态更新为 '已缴费'
            ord_obj.payment_status = '已缴费'
            ord_obj.save()

            return Action.success(f"订单 '{ord_obj.id}' 缴费成功，状态已更新为 '已缴费'。")
    except order.DoesNotExist:
        return Action.fail("要缴费的订单不存在。")
    except ValueError as ve:  # 捕获自定义的库存不足或药品不存在错误
        logger.warning("Business validation failed in orderPay: %s", ve)
        return Action.fail(str(ve))
    except Exception as e:
        logger.exception("orderPay failed for order_id=%s: %s", order_id, e)
        return Action.fail(f"缴费失败: {str(e)}")


@api_view(['POST'])
# 取号功能
def orderTakeNumber(request):
    order_id = request.POST.get('id')

    if not order_id:
        return Action.fail("缺少订单ID参数")

    try:
        with transaction.atomic():
            ord_obj = order.objects.get(id=order_id)

            # 检查是否已缴费 (通常取号需要先缴费)
            if ord_obj.payment_status != '已缴费':
                return Action.fail(f"订单 '{ord_obj.id}' 尚未缴费，请先完成缴费。")

            # 匹配模型字段名 numbertake_status
            if ord_obj.numbertake_status == '已取号':
                return Action.fail(f"订单 '{ord_obj.id}' 已是已取号状态，无需重复取号。")

            # 将取号状态更新为 '已取号'
            # 匹配模型字段名 numbertake_status
            ord_obj.numbertake_status = '已取号'
            ord_obj.save()

            return Action.success(f"订单 '{ord_obj.id}' 取号成功，状态已更新为 '已取号'。")
    except order.DoesNotExist:
        return Action.fail("要取号的订单不存在。")
    except Exception as e:
        return Action.fail(f"取号失败: {str(e)}")