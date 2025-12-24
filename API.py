import os
import glob
import logging
from flask import Flask, request, jsonify

# --- تنظیمات لاگینگ (اضافه شده طبق درخواست قبلی برای پایداری) ---
logging.basicConfig(
    filename='api_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

app = Flask(__name__)

# *** خط مهم برای حل مشکل فارسی ***
# این تنظیم باعث می‌شود Flask کاراکترهای فارسی را به کد تبدیل نکند و همانطور که هست بفرستد
app.json.ensure_ascii = False 

DATA_FOLDER = 'data'

# اطمینان از وجود فولدر دیتا
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

@app.route('/get', methods=['GET'])
def get_latest_file():
    try:
        # پیدا کردن تمام فایل‌های txt در فولدر data
        list_of_files = glob.glob(os.path.join(DATA_FOLDER, '*.txt'))
        
        if not list_of_files:
            return jsonify({"status": "error", "message": "No files found"}), 404

        # پیدا کردن جدیدترین فایل بر اساس زمان تغییر
        latest_file = max(list_of_files, key=os.path.getctime)
        file_name = os.path.basename(latest_file)

        # خواندن محتوا
        content = ""
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            return jsonify({"status": "error", "message": f"Could not read file: {str(e)}"}), 500

        # ارسال پاسخ (حالا فارسی را درست نشان می‌دهد)
        return jsonify({
            "status": "success",
            "file_name": file_name,
            "content": content
        })

    except Exception as e:
        # ثبت خطا در لاگ و جلوگیری از توقف
        logging.error(f"Server Error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

@app.route('/delete', methods=['DELETE', 'GET', 'POST'])
def delete_file():
    try:
        # دریافت نام فایل از پارامترهای URL یا JSON
        file_name = request.args.get('filename') or request.json.get('filename')

        if not file_name:
            return jsonify({"status": "error", "message": "filename parameter is missing"}), 400

        # جلوگیری از Directory Traversal
        safe_name = os.path.basename(file_name)
        file_path = os.path.join(DATA_FOLDER, safe_name)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return jsonify({"status": "success", "message": f"File {safe_name} deleted successfully"})
            except Exception as del_err:
                 logging.error(f"Error deleting file: {del_err}")
                 return jsonify({"status": "error", "message": f"Failed to delete: {str(del_err)}"}), 500
        else:
            return jsonify({"status": "error", "message": "File not found"}), 404

    except Exception as e:
        logging.error(f"Server Error in delete: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # اجرای سرور روی پورت 5000
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)