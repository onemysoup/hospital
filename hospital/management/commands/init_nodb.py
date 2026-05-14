from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Initialize SQLite tables for local no-DB preview mode."

    def handle(self, *args, **options):
        engine = connection.settings_dict.get("ENGINE", "")
        if "sqlite3" not in engine:
            raise CommandError("init_nodb 仅支持 sqlite 配置，请在 .env 中设置 DB_ENGINE=sqlite 后再运行。")

        create_table_sql = [
            """
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                password VARCHAR(45) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_patient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                id_card VARCHAR(45) NOT NULL,
                phone VARCHAR(45) NOT NULL,
                password VARCHAR(45) NOT NULL,
                sex SMALLINT NOT NULL,
                age SMALLINT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS department (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                registration_fee DECIMAL(10, 2) NOT NULL,
                doctor_num SMALLINT NOT NULL DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_doctor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                id_card VARCHAR(45) NOT NULL,
                department_id SMALLINT NOT NULL,
                password VARCHAR(45) NOT NULL,
                status SMALLINT NOT NULL DEFAULT 1,
                shift_status VARCHAR(50) DEFAULT '值班'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS medicine (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                unit VARCHAR(45) NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS `order` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id SMALLINT NOT NULL,
                department_id SMALLINT NOT NULL,
                readme VARCHAR(200) NOT NULL,
                registration_fee DECIMAL(10, 2) NOT NULL,
                doctor_id SMALLINT NOT NULL,
                numbertake_status VARCHAR(50) NOT NULL DEFAULT '未取号',
                order_advice VARCHAR(400) NOT NULL,
                medicine_list VARCHAR(200) NOT NULL,
                total_cost DECIMAL(10, 2) NOT NULL DEFAULT 0,
                payment_status VARCHAR(50) NOT NULL DEFAULT '未缴费',
                status SMALLINT NOT NULL DEFAULT 1,
                time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
        ]

        with transaction.atomic():
            with connection.cursor() as cursor:
                for sql in create_table_sql:
                    cursor.execute(sql)

                cursor.execute("SELECT COUNT(*) FROM admin")
                admin_count = cursor.fetchone()[0]
                if admin_count == 0:
                    cursor.execute(
                        "INSERT INTO admin (name, password) VALUES (%s, %s)",
                        ["admin", "123456"],
                    )

                cursor.execute("SELECT COUNT(*) FROM department")
                department_count = cursor.fetchone()[0]
                if department_count == 0:
                    cursor.execute(
                        "INSERT INTO department (name, registration_fee, doctor_num) VALUES (%s, %s, %s)",
                        ["内科", 10.00, 0],
                    )

                cursor.execute("SELECT COUNT(*) FROM user_doctor")
                doctor_count = cursor.fetchone()[0]
                if doctor_count == 0:
                    cursor.execute(
                        "INSERT INTO user_doctor (name, id_card, department_id, password, status, shift_status) VALUES (%s, %s, %s, %s, %s, %s)",
                        ["演示医生", "2001", 1, "123456", 1, "值班"],
                    )

                cursor.execute("SELECT COUNT(*) FROM user_patient")
                patient_count = cursor.fetchone()[0]
                if patient_count == 0:
                    cursor.execute(
                        "INSERT INTO user_patient (name, id_card, phone, password, sex, age) VALUES (%s, %s, %s, %s, %s, %s)",
                        ["演示患者", "1001", "13800000001", "123456", 1, 20],
                    )

        self.stdout.write(self.style.SUCCESS("SQLite 预览表初始化完成。默认账号：admin/123456，医生(身份证:2001)/123456，患者(身份证:1001)/123456"))
