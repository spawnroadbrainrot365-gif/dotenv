import os
from config import get_roblox_cookie, set_roblox_cookie
from roblox_api import upload_asset

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("========================================")
    print("   Roblox Asset Manager - Python Edition")
    print("========================================\n")

    cookie = get_roblox_cookie()
    if not cookie:
        print("[!] لم يتم العثور على كوكي محفوظ.")
        cookie = input("أدخل .ROBLOSECURITY الخاص بك: ").strip()
        set_roblox_cookie(cookie)
        print("[+] تم حفظ الكوكي بنجاح.\n")

    while True:
        print("1. رفع أصل جديد (Image, Audio, etc.)")
        print("2. تغيير الكوكي")
        print("3. خروج")
        
        choice = input("\nاختر رقم العملية: ")

        if choice == "1":
            path = input("مسار الملف (مثال: image.png): ").strip('"')
            if not os.path.exists(path):
                print("[!] الملف غير موجود!")
                continue
            
            name = input("اسم الأصل: ")
            desc = input("وصف الأصل: ")
            a_type = input("نوع الأصل (Image/Audio/Decal): ")
            
            print("\n[~] جاري الرفع...")
            success, result = upload_asset(cookie, path, a_type, name, desc)
            
            if success:
                print(f"[+] نجح الرفع! البيانات: {result}")
            else:
                print(f"[!] فشل الرفع: {result}")
                
        elif choice == "2":
            cookie = input("أدخل الكوكي الجديد: ").strip()
            set_roblox_cookie(cookie)
            print("[+] تم التحديث.")
            
        elif choice == "3":
            print("وداعاً!")
            break
        
        input("\nاضغط Enter للاستمرار...")
        clear_screen()

if __name__ == "__main__":
    main()
