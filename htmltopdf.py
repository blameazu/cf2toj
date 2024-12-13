import sys
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def html_to_pdf(input_html, output_pdf):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)

        print(f"Input HTML path: {os.path.abspath(input_html)}")
        
        if not os.path.isfile(input_html):
            print(f"Error: The file {input_html} does not exist.")
            return

        driver.get(f"file:///{os.path.abspath(input_html)}")

        time.sleep(2)

        result = driver.execute_cdp_cmd('Page.printToPDF', {
            'format': 'A4',
        })

        if 'data' in result:
            pdf_data = base64.b64decode(result['data'])

            with open(output_pdf, 'wb') as f:
                f.write(pdf_data)

            print(f"PDF successfully created at {output_pdf}")
        
        driver.quit()

    except Exception as e:
        print(f"Failed to generate PDF: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python htmltopdf.py <input_html_file> <output_pdf_file>")
        sys.exit(1)

    input_html = sys.argv[1]
    output_pdf = sys.argv[2]

    html_to_pdf(input_html, output_pdf)
