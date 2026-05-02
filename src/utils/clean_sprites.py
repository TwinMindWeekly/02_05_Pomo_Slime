from PIL import Image
import os

def clean_sprite_sheet(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Thay đổi màu trắng (gần trắng) thành trong suốt
        # AI thường tạo nền không phải trắng tinh (255,255,255) mà hơi lệch xíu
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Cleaned sprite sheet saved to {output_path}")

if __name__ == "__main__":
    brain_dir = r"C:\Users\admin\.gemini\antigravity\brain\aadac9d5-c90a-4c0f-9677-276eded3a39b"
    assets_dir = r"d:\Workspace\Project\Week2\CoreBuddy\assets\sprites"
    
    skins = {
        "slime_sheet_blue.png": "slime_sheet_blue_v1_1777711412077.png",
        "slime_sheet_red.png": "slime_sheet_red_v1_1777711475234.png",
        "slime_sheet_gold.png": "slime_sheet_gold_v1_1777711620067.png"
    }
    
    for output_name, input_name in skins.items():
        input_path = os.path.join(brain_dir, input_name)
        output_path = os.path.join(assets_dir, output_name)
        if os.path.exists(input_path):
            clean_sprite_sheet(input_path, output_path)
