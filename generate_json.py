import os
import json
import subprocess
from datetime import datetime
import pytz

details_folder = 'DETAILS'
logos_folder = 'LOGOS'
base_logo_url = 'https://cdn.jsdelivr.net/gh/splshameem420/IPTV@main/LOGOS/'
bd_timezone = pytz.timezone('Asia/Dhaka')



available_logos = os.listdir(logos_folder) if os.path.exists(logos_folder) else []

def get_file_last_commit_date(filepath):
    try:
        cmd = ['git', 'log', '-1', '--format=%ct', filepath]
        timestamp = subprocess.check_output(cmd).decode('utf-8').strip()
        if timestamp:
            dt = datetime.fromtimestamp(int(timestamp), bd_timezone)
            return dt.strftime('%d-%m-%Y %I:%M %p (Bangladesh Time)')
    except Exception:
        pass
    return datetime.now(bd_timezone).strftime('%d-%m-%Y %I:%M %p (Bangladesh Time)')

def get_image_url(channel_name):
    for ext in ['.png', '.jpg', '.svg', '.webp']:
        file_with_ext = f"{channel_name}{ext}"
        if file_with_ext in available_logos:
            url_friendly_name = file_with_ext.replace(" ", "%20")
            return f"{base_logo_url}{url_friendly_name}"
    return ""

def generate_json():
    final_list = []
    
    if not os.path.exists(details_folder):
        print(f"Error: {details_folder} folder not found!")
        return

    for filename in os.listdir(details_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(details_folder, filename)
            last_date = get_file_last_commit_date(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = {}
                for line in f:
                    if ':' in line:
                        clean_line = line.split(']')[-1].strip() if ']' in line else line.strip()
                        if ':' in clean_line:
                            key, val = clean_line.split(':', 1)
                            data[key.strip().upper()] = val.strip()

            if 'CHANNEL_NAME' in data:
                name = data['CHANNEL_NAME']
                channel_info = {
                    "NAME": name,
                    "LOGO_URL": get_image_url(name),
                    "COUNTRY": data.get('COUNTRY', ''),
                    "MAIN_CATEGORY": data.get('MAIN_CATEGORY', ''),
                    "SUB_CATEGORY": data.get('SUB_CATEGORY', ''),
                    "last_update": last_date
                }
                final_list.append(channel_info)
                
    overall_update = datetime.now(bd_timezone).strftime('%d-%m-%Y %I:%M %p')
    final_output = {
        "database_last_update": overall_update,
        "total_channels": len(final_list),
        "channels": final_list
    }

    with open('database.json', 'w', encoding='utf-8') as jf:
        json.dump(final_output, jf, indent=4, ensure_ascii=False)

    print(f"Success! {len(final_list)} ti channel process hoyeche (Country shoho).")

if __name__ == "__main__":
    generate_json()