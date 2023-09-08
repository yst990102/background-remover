import os
import gradio as gr
import tempfile
import rembg
from PIL import Image
import atexit

UPLOAD_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def remove_background(input_path, output_path):
    input = Image.open(input_path)
    output = rembg.remove(input)
    output.save(output_path)

def remove_background_gradio(input_image):
    with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_FOLDER, suffix=".webp") as temp_input_file:
        input_path = temp_input_file.name
        input_image.save(input_path)
    with tempfile.NamedTemporaryFile(delete=False, dir=OUTPUT_FOLDER, suffix=".webp") as temp_output_file:
        output_path = temp_output_file.name
    remove_background(input_path, output_path)
    return Image.open(output_path)

def cleanup_folders():
    for file in os.scandir(UPLOAD_FOLDER):
        os.remove(file.path)
    for file in os.scandir(OUTPUT_FOLDER):
        os.remove(file.path)

if __name__ == '__main__':
    # 清理函数
    atexit.register(cleanup_folders)  # 注册清理函数
    
    examples = [f"examples/{file.name}" for file in os.scandir('./examples')]
    
    iface = gr.Interface(
        fn=remove_background_gradio,
        inputs=gr.inputs.Image(type='pil', label='Input Image'),
        outputs=gr.outputs.Image(type='pil', label='Output Image'),
        live=True,
        title='Background Remover',
        description='Upload an image and remove the background using Rembg.',
        examples=examples
    )
    iface.launch(share=False, server_name="0.0.0.0")
