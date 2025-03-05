from PIL import Image, ImageDraw

def drawStroke(strokes):

    #Define size of image
    size = 800

    # Create canvas with fixed dimensions
    canvas_size = (size, size)
    image = Image.new('RGB', canvas_size, 'white')
    draw = ImageDraw.Draw(image)

    # Calculate bounds across all strokes
    all_x = [x for stroke in strokes for x in stroke['x']]
    all_y = [y for stroke in strokes for y in stroke['y']]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Set padding and scale
    padding = 30
    content_width = max_x - min_x + padding * 2
    content_height = max_y - min_y + padding * 2
    scale = min((size - padding * 2) / content_width, (size - padding * 2) / content_height)

    # Center the content
    translate_x = (size - content_width * scale) / 2 - min_x * scale
    translate_y = (size - content_height * scale) / 2 - min_y * scale

    # Draw all strokes
    for i, stroke in enumerate(strokes):

        scaled_x = [(x * scale + translate_x) for x in stroke['x']]
        scaled_y = [(y * scale + translate_y) for y in stroke['y']]

        #Increase size of dots for better visibility for Gemini
        if len(scaled_x) < 3:
            x = scaled_x[0]
            y = scaled_y[0] 
            draw.ellipse([x-5, y-5, x+5, y+5], fill='black')
        else:
            for i in range(len(scaled_x) - 1):
                draw.line([(scaled_x[i], scaled_y[i]), (scaled_x[i + 1], scaled_y[i + 1])], fill='black', width=3)

    return image
