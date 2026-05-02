from PIL import Image, ImageDraw
import os

os.makedirs('assets/sprites', exist_ok=True)
os.makedirs('assets/sounds', exist_ok=True)

# Colors
colors = {
    "happy": (166, 227, 161, 255),   # Green
    "sad": (137, 180, 250, 255),     # Blue
    "angry": (243, 139, 168, 255),   # Red
    "evolving": (249, 226, 175, 255) # Yellow/Gold
}

# Generate a bouncing circular slime for each color
for name, color in colors.items():
    frames = []
    # 10 frames for a bounce animation
    for i in range(10):
        # Create a transparent image 150x150
        img = Image.new('RGBA', (150, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate bounce offset
        # Y goes from 0 to 20 and back to 0
        if i < 5:
            offset_y = i * 4
        else:
            offset_y = (9 - i) * 4
            
        # Draw the circle (slime body)
        x0, y0 = 25, 25 + offset_y
        x1, y1 = 125, 125 + offset_y
        
        # Squeeze effect at bottom
        if i == 5:
            y0 += 10
            x0 -= 5
            x1 += 5
            
        draw.ellipse([x0, y0, x1, y1], fill=color)
        
        # Draw eyes
        eye_color = (30, 30, 46, 255)
        
        if name == "angry":
            # Angry eyes \ /
            draw.line([50, 50+offset_y, 65, 60+offset_y], fill=eye_color, width=4)
            draw.line([100, 50+offset_y, 85, 60+offset_y], fill=eye_color, width=4)
        elif name == "sad":
            # Sad eyes / \
            draw.line([50, 60+offset_y, 65, 50+offset_y], fill=eye_color, width=4)
            draw.line([100, 60+offset_y, 85, 50+offset_y], fill=eye_color, width=4)
        else:
            # Normal round eyes
            draw.ellipse([50, 55+offset_y, 60, 65+offset_y], fill=eye_color)
            draw.ellipse([90, 55+offset_y, 100, 65+offset_y], fill=eye_color)
            
        # Add frame
        frames.append(img)
        
    # Save as animated GIF
    frames[0].save(
        f'assets/sprites/{name}.gif',
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        disposal=2 # Clear frame before drawing next
    )

print("Generated GIFs successfully in assets/sprites/")
