from fpdf import FPDF
from PIL import Image
import os

class PDFMaker:
    def __init__(self, folder_name):
        self.folder_name = folder_name
    
    def convert_to_jpg(self, image_path):
        """Қайта JPG форматқа келтіреміз."""
        img = Image.open(image_path)
        rgb_im = img.convert('RGB')  # Jpg үшін RGB ға айналдырамыз
        new_image_path = image_path.rsplit('.', 1)[0] + '.jpg'  # Форматын .jpg-қа ауыстырамыз
        rgb_im.save(new_image_path, quality=40)  # Сапасын 40 пайызға түсіреміз
        return new_image_path
    
    def create_pdf(self):
        # PDF бетіне өлшемін қоямыз (1191x1684 пиксел)
        pdf = FPDF(unit="pt", format=[1191, 1684])  # (1 pt = 1/72 inch)
        
        # Папкадағы беттерді аламыз
        img_list = [x for x in os.listdir(self.folder_name) if x.endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff'))]
        
        # JPGға айналдырып, PDFке саламыз
        for img in img_list:
            pdf.add_page()
            image_path = os.path.join(self.folder_name, img)
            
            image_path = self.convert_to_jpg(image_path) #Жпгға айналдыру
            
            pdf.image(image_path, x=0, y=0, w=1191, h=1684)

        # Сақтау
        output_pdf_path = f"{self.folder_name}.pdf"
        pdf.output(output_pdf_path)
