import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

def create_social_preview():
    # Configuration
    WIDTH, HEIGHT = 1280, 640
    # Use a high-contrast gradient or solid dark background
    BG_COLOR = "#0B1120"  # Very Dark Slate (almost black)
    TEXT_COLOR = "#F8FAFC" # Slate 50 (Very bright white)
    SUBTITLE_COLOR = "#CBD5E1" # Slate 300 (Light grey)
    ACCENT_COLOR = "#3B82F6"  # Blue 500 (Vibrant Blue)
    ACCENT_BG = "#1E3A8A" # Blue 900 (Dark Blue for tags)
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, "docs", "images")
    output_path = os.path.join(images_dir, "social-preview.png")
    
    mascot_path = os.path.join(images_dir, "arthor-agent-mascot.png")
    screenshot_path = os.path.join(images_dir, "streamlit-dashboard.png")
    
    # Create base image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts (fallback to default if not found)
    try:
        # MacOS system fonts
        title_font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 100, index=1) # Bold
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 40)
        tag_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 30)
    except IOError:
        try:
            # Linux/Other
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
            subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 40)
            tag_font = ImageFont.truetype("DejaVuSansMono.ttf", 30)
        except IOError:
            # Fallback
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            tag_font = ImageFont.load_default()
            print("Warning: Custom fonts not found, using default.")

    # --- Left Side: Branding ---
    
    # Draw Title
    draw.text((80, 150), "Arthor Agent", font=title_font, fill=TEXT_COLOR)
    
    # Draw Subtitle - Improved contrast
    draw.text((80, 270), "Automated Security Assessment", font=subtitle_font, fill=SUBTITLE_COLOR)
    draw.text((80, 320), "with LLMs & RAG", font=subtitle_font, fill=SUBTITLE_COLOR)
    
    # Draw Tags/Badges (Simulated) - High contrast style
    tags = ["MCP Ready", "Local LLM", "Python"]
    tag_x = 80
    tag_y = 420
    for tag in tags:
        # Draw pill background
        bbox = draw.textbbox((tag_x, tag_y), tag, font=tag_font)
        padding = 15
        pill_box = (tag_x, tag_y, tag_x + (bbox[2]-bbox[0]) + padding*2, tag_y + (bbox[3]-bbox[1]) + padding*2)
        # Use ACCENT_BG for fill to make text pop
        draw.rounded_rectangle(pill_box, radius=10, fill=ACCENT_BG, outline=ACCENT_COLOR, width=2)
        # Use TEXT_COLOR (White) for text instead of accent color for better readability
        draw.text((tag_x + padding, tag_y + padding), tag, font=tag_font, fill=TEXT_COLOR)
        tag_x += (bbox[2]-bbox[0]) + padding*2 + 30

    # Draw Mascot (if exists)
    if os.path.exists(mascot_path):
        try:
            mascot = Image.open(mascot_path).convert("RGBA")
            # Resize mascot
            mascot.thumbnail((200, 200))
            # Paste mascot
            img.paste(mascot, (80, 50), mascot)
            # Move title down if mascot is there? No, let's put mascot top-right of the text area?
            # Actually, let's put mascot next to title or above.
            # Let's re-layout: Mascot at (80, 50) is overlapping title at (80, 150) potentially?
            # Title y=150. Mascot size 200. 50+200=250. Overlap.
            # Let's put mascot to the right of the text block or top-left.
            # Revised: Mascot Top-Left (50, 50), Title starts at x=50, y=260?
            # Or Mascot at bottom left.
            # Let's put Mascot at (80, 40) scaled to 100x100
            mascot.thumbnail((100, 100))
            img.paste(mascot, (80, 40), mascot)
            # Adjust Text Positions
            draw.text((200, 40), "Arthor Agent", font=title_font, fill=TEXT_COLOR)
            # Reset subtitle positions
            draw.text((200, 160), "Automated Security Assessment", font=subtitle_font, fill=SUBTITLE_COLOR)
            draw.text((200, 210), "with LLMs & RAG", font=subtitle_font, fill=SUBTITLE_COLOR)
            
            # Reset tags
            tag_x = 200
            tag_y = 300
            for tag in tags:
                bbox = draw.textbbox((tag_x, tag_y), tag, font=tag_font)
                padding = 10
                pill_box = (tag_x, tag_y, tag_x + (bbox[2]-bbox[0]) + padding*2, tag_y + (bbox[3]-bbox[1]) + padding*2)
                draw.rounded_rectangle(pill_box, radius=10, fill=ACCENT_BG, outline=ACCENT_COLOR, width=2)
                draw.text((tag_x + padding, tag_y + padding), tag, font=tag_font, fill=TEXT_COLOR)
                tag_x += (bbox[2]-bbox[0]) + padding*2 + 20
                
        except Exception as e:
            print(f"Could not process mascot: {e}")

    # --- Right Side: Screenshot ---
    if os.path.exists(screenshot_path):
        try:
            screenshot = Image.open(screenshot_path).convert("RGBA")
            # Resize to fit nicely
            # Max height 500, max width 700
            screenshot.thumbnail((800, 500))
            
            # Add rounded corners to screenshot
            mask = Image.new("L", screenshot.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle((0, 0) + screenshot.size, radius=20, fill=255)
            
            # Add shadow/glow
            # Create a larger image for shadow
            shadow_size = (screenshot.width + 40, screenshot.height + 40)
            shadow = Image.new("RGBA", shadow_size, (0,0,0,0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rounded_rectangle((10, 10, shadow_size[0]-10, shadow_size[1]-10), radius=20, fill=(0,0,0, 100))
            shadow = shadow.filter(ImageFilter.GaussianBlur(10))
            
            # Paste shadow
            screenshot_x = 1280 - screenshot.width - 50
            screenshot_y = (640 - screenshot.height) // 2
            
            img.paste(shadow, (screenshot_x - 20, screenshot_y - 20), shadow)
            img.paste(screenshot, (screenshot_x, screenshot_y), mask)
            
        except Exception as e:
            print(f"Could not process screenshot: {e}")

    # Save
    img.save(output_path)
    print(f"Social preview saved to {output_path}")

if __name__ == "__main__":
    create_social_preview()
