from PIL import Image, ImageDraw, ImageFont

def create_placeholder(filename, text, size=(1200, 800), color=(50, 50, 50)):
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not found
    try:
        # Try loading Arial or similar if available
        # font = ImageFont.truetype("arial.ttf", 60)
        # On macOS/Linux default path might vary, let's just use default or load specific if needed
        # Simple default font is very small, let's try to load something bigger or just draw text
        pass
    except:
        pass
        
    # Draw a border
    d.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline=(200, 200, 200), width=5)
    
    # Draw text centered
    # Since we might not have a TTF font easily available, let's draw text simply
    # For better quality we should load a font, but for placeholder default is fine
    # Or just use a simple drawing
    d.text((size[0]//2 - 100, size[1]//2), text, fill=(255, 255, 255), anchor="mm", align="center")
    
    img.save(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_placeholder("docs/images/streamlit-dashboard.png", "Streamlit Dashboard Screenshot Placeholder\n(Please replace with actual screenshot)")
    create_placeholder("docs/images/streamlit-workbench.png", "Assessment Workbench Screenshot Placeholder\n(Please replace with actual screenshot)")
