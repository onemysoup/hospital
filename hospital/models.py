from django.db import models

# 管理员类
class admin(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=45) # 姓名
    password = models.CharField(max_length=45) # 密码

    class Meta:
        managed = False
        db_table = 'admin'

# 患者类
class user_patient(models.Model):
    sex_choices = (
        (0, "女"),
        (1, "男")
    )
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=45) # 姓名
    id_card = models.CharField(max_length=45) # 身份证
    phone = models.CharField(max_length=45) # 电话
    password = models.CharField(max_length=45) # 密码
    sex = models.SmallIntegerField(choices=sex_choices) # 性别
    age = models.SmallIntegerField() # 年龄

    class Meta:
        managed = False
        db_table = 'user_patient'

# 医生类
class user_doctor(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=45) # 姓名
    id_card = models.CharField(max_length=45) # 身份证
    department_id = models.SmallIntegerField() # 科室
    password = models.CharField(max_length=45) # 密码
    status = models.SmallIntegerField(default=1) # 状态
    shift_status = models.CharField(max_length=50, default='值班', null=True, blank=True)#值班

    class Meta:
        managed = False
        db_table = 'user_doctor'

    def __str__(self):
        return self.name

# 科室类
class department(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=45) # 名称
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2) # 挂号费
    doctor_num = models.SmallIntegerField(default=0) # 医生数

    class Meta:
        managed = False
        db_table = 'department'

    def __str__(self):
        return self.name

# 药品类
class medicine(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=45) # 名称
    price = models.DecimalField(max_digits=10, decimal_places=2) # 单价
    unit = models.CharField(max_length=45) # 单位
    quantity = models.IntegerField(default=0)#数量

    class Meta:
        managed = False
        db_table = 'medicine'

    def __str__(self):
        return self.name

# 就诊、挂号
class order(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    patient_id = models.SmallIntegerField() # 患者id
    department_id = models.SmallIntegerField() # 科室
    readme = models.CharField(max_length=200) # 自述
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2) # 挂号费
    doctor_id = models.SmallIntegerField() # 医生id
    numbertake_status = models.CharField(max_length=50, default='未取号', verbose_name="取号状态")#取号
    order_advice = models.CharField(max_length=400) # 医嘱
    medicine_list = models.CharField(max_length=200) # 药列表
    total_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0) # 总费用
    payment_status = models.CharField(max_length=50, default='未缴费',verbose_name="缴费状态")  # 假设是字符串，例如 '未缴费', '已缴费'
    status = models.SmallIntegerField(default=1) # 状态
    time = models.DateTimeField(auto_now_add=True) # 创建时间

    class Meta:
        managed = False
        db_table = 'order'