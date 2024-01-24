from PIL import Image, ImageDraw
import os


def draw_scale_bar(image, pixel_size, scale_bar_length):
    width, height = image.size
    scale_bar_width = int(scale_bar_length / pixel_size)

    # Create a new transparent image with space for the scale bar
    new_image = Image.new("RGBA", (width + scale_bar_width, height), (255, 255, 255, 0))

    # Paste the original image onto the new image
    new_image.paste(image, (0, 0))

    # Draw the scale bar
    draw = ImageDraw.Draw(new_image)
    scale_bar_start = width
    scale_bar_end = width + scale_bar_width
    draw.line([(scale_bar_start, 10), (scale_bar_end, 10)], fill="black", width=5)

    return new_image


def process_images(input_folder, output_folder, pixel_size, scale_bar_length):
    os.makedirs(output_folder, exist_ok=True)
    os.listdir(output_folder)
    for filename in os.listdir(input_folder):
        print(filename)
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Open the image
            original_image = Image.open(input_path)

            # Draw the scale bar on the image
            result_image = draw_scale_bar(original_image, pixel_size, scale_bar_length)
            print(result_image)
            # Save the resulting image
            result_image.save(output_path)


if __name__ == "__main__":
    input_folder = "../../resources/images"
    output_folder = "../../resources/scaled"
    pixel_size = 5  # microns
    scale_bar_length = 50  # microns

    process_images(input_folder, output_folder, pixel_size, scale_bar_length)