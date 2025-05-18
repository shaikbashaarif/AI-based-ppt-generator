from PIL import Image, ImageDraw, ImageFont
import os

class ImageGenerator:
    def __init__(self, output_dir="output/images"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_image(self, text, index, filename_prefix="slide"):
        img = Image.new('RGB', (800, 400), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (800 - text_width) / 2
        y = (400 - text_height) / 2

        draw.text((x, y), text, fill=(0, 0, 0), font=font)

        # ✅ Save with filename reference to avoid overwriting
        sanitized_prefix = filename_prefix.replace(" ", "_").replace(".", "_")
        img_path = os.path.join(self.output_dir, f"{sanitized_prefix}_image_{index}.png")
        img.save(img_path)
        return img_path


    def generate_images_for_summaries(self, summaries):
        images_by_file = {}
        for filename, summary in summaries.items():
            summary_points = summary.split("\n")
            image_paths = []
            for i, point in enumerate(summary_points):
                if point.strip():
                    img_path = self.generate_image(point, i, filename_prefix=filename)
                    image_paths.append(img_path)
            images_by_file[filename] = image_paths
        return images_by_file
