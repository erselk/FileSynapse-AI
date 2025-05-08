from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(size=256):
    """Create the application logo."""
    # Create a new image with a transparent background
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw the main circle
    circle_color = (13, 71, 161)  # Dark blue
    draw.ellipse([10, 10, size-10, size-10], fill=circle_color)
    
    # Draw the synapse pattern
    synapse_color = (255, 255, 255)  # White
    center = size // 2
    radius = (size - 20) // 2
    
    # Draw the main connections
    for angle in range(0, 360, 45):
        x1 = center + int(radius * 0.3 * cos(angle))
        y1 = center + int(radius * 0.3 * sin(angle))
        x2 = center + int(radius * 0.8 * cos(angle))
        y2 = center + int(radius * 0.8 * sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=synapse_color, width=3)
        
        # Draw connection points
        draw.ellipse([x1-5, y1-5, x1+5, y1+5], fill=synapse_color)
        draw.ellipse([x2-5, y2-5, x2+5, y2+5], fill=synapse_color)
    
    # Save the logo in different sizes
    sizes = [16, 32, 48, 64, 128, 256]
    for s in sizes:
        resized = image.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'logo_{s}.ico', format='ICO')
        resized.save(f'logo_{s}.png', format='PNG')
    
    # Save the original size
    image.save('logo_256.ico', format='ICO')
    image.save('logo_256.png', format='PNG')

if __name__ == '__main__':
    from math import cos, sin
    create_logo() 