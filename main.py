import flet as ft
import requests

# بيانات Backendless
APP_ID = "1C784CDF-FFCD-407D-AF62-CB89D7A2C66A"
API_KEY = "CDA8576F-8142-468A-BCE6-02571B945F75"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}/data/Posts"


def main(page: ft.Page):
    page.title = "تطبيق مشترك"
    page.scroll = "auto"
    page.horizontal_alignment = "center"
    page.window.height = 640
    page.window.width = 360
    page.window.top = 10
    page.window.left = 960
    # الحقول
    name_input = ft.TextField(label="اسم المستخدم", width=300)
    email_input = ft.TextField(label="البريد الإلكتروني", width=300)
    phone_input = ft.TextField(label="رقم الهاتف", width=300)
    message_input = ft.TextField(label="الرسالة", multiline=True, width=300)

    # حاوية عرض البيانات
    data_container = ft.Column()

    # دالة تحميل البيانات من Backendless
    def load_data():
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            users = response.json()
            print("📥 Data from Backendless:", users)  # اطبع كل البيانات للتأكد
            data_container.controls.clear()

            if users:
                for user in users:
                    print("➡ سجل واحد:", user)  # اطبع كل سجل لحاله

                    # جرب نعرض القيم
                    user_card = ft.Container(
                        content=ft.Column([
                            ft.Text(f"Name: {user.get('name')}", color="yellow"),
                            ft.Text(f"Email: {user.get('email')}", color="yellow"),
                            ft.Text(f"Phone: {user.get('phone')}", color="yellow"),
                            ft.Text(f"Message: {user.get('message')}", color="white"),
                        ]),
                        bgcolor="black",
                        padding=15,
                        border_radius=10,
                        margin=10,
                        width=300
                    )
                    data_container.controls.append(user_card)
            else:
                data_container.controls.append(ft.Text("لا توجد بيانات بعد.", color="red"))

            page.update()

    # دالة النشر
    def on_submit_click(e):
        data = {
            "name": name_input.value,
            "email": email_input.value,
            "phone": phone_input.value,
            "message": message_input.value,
        }
        print("📤 Sending data:", data)  # اطبع البيانات المرسلة
        response = requests.post(BASE_URL, json=data)
        print("📥 Response:", response.status_code, response.text)  # اطبع الرد
        if response.status_code == 200:
            page.add(ft.Text("✅ تم حفظ البيانات بنجاح", color="green"))
            load_data()
        else:
            page.add(ft.Text("❌ خطأ في الحفظ", color="red"))

    # زر النشر
    submit_button = ft.ElevatedButton("نشر", on_click=on_submit_click, bgcolor="blue", color="white")

    # واجهة التطبيق
    page.add(
        ft.Text("تطبيق نشر مشترك", size=20, color="blue"),
        name_input,
        email_input,
        phone_input,
        message_input,
        submit_button,
        ft.Text("المنشورات:", size=18, color="black"),
        data_container
    )

    # تحميل البيانات عند فتح التطبيق
    load_data()


# تشغيل التطبيق
ft.app(target=main)
