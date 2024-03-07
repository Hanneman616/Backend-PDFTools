from flask import Flask, request, send_file, jsonify
from pylovepdf.tools.imagetopdf import ImageToPdf
from pylovepdf.tools.merge import Merge
from pylovepdf.tools.compress import Compress
from pylovepdf.tools.officepdf import OfficeToPdf
import os


app = Flask(__name__)

@app.route('/jpg-pdf', methods=['POST'])
def jpg_a_pdf():
    try:
        file = request.files['file']
        
        # se guarda el archivo en el directorio de trabajo
        file_path = os.path.join(os.getcwd(), file.filename)
        file.save(file_path)

        pdf_path = convert_image_to_pdf(file_path)
        
        # se elimina el archivo despues de la conversion
        os.remove(file_path)
        
#        if pdf_path:
#            return f"PDF convertido: {pdf_path}", 200
#        else:
#            return "Error al convertir la imagen a PDF", 500
#    except Exception as e:
#        print("Error al convertir el archivo:", e)
#        return "Error al convertir el archivo", 500
        if pdf_path:
            # Instead of downloading the file, return it as a response
            with open(pdf_path, 'rb') as file:
                return jsonify({
                    'success': True,
                    'file': file.read().decode('latin-1')
                }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al convertir la imagen a PDF'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al convertir el archivo'
        }), 500


@app.route('/merge', methods=['POST'])
def merge():
    try:
        ## se guarda el array de archivos en el directorio de trabajo
        files = []
        for file in request.files.getlist('files'):
            file_path = os.path.join(os.getcwd(), file.filename)
            file.save(file_path)
            files.append(file_path)

        pdf_path = merge_pdfs(files)

        # se eliminan los archivos despues de la conversion
        for file in files:
            os.remove(file)
        # se retorna el archivo unido
#        if pdf_path:
#            return send_file(pdf_path, as_attachment=True), 200
#        else:
#            return "Error al fusionar los archivos PDF", 500
#    except Exception as e:
#        print("Error al unir los archivos:", e)
#        return "Error al unir los archivos", 500
        if pdf_path:
                # Instead of downloading the file, return it as a response
                with open(pdf_path, 'rb') as file:
                    return jsonify({
                        'success': True,
                        'file': file.read().decode('latin-1')
                    }), 200
        else:
                return jsonify({
                    'success': False,
                    'message': 'Error al fusionar los archivos PDF'
                }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al unir los archivos'
        }), 500
                

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        
        # se guarda el archivo en el directorio de trabajo
        file_path = os.path.join(os.getcwd(), file.filename)
        file.save(file_path)

        pdf_path = compress_pdf(file_path)
        
        # se elimina el archivo despues de la conversion
        os.remove(file_path)
        
#        if pdf_path:
#            return f"PDF comprimido: {pdf_path}", 200
#        else:
#            return "Error al comprimir el PDF", 500
#    except Exception as e:
#        print("Error al comprimir el archivo:", e)
#        return "Error al comprimir el archivo", 500

        if pdf_path:
            # retornar el archivo comprimido
            with open(pdf_path, 'rb') as file:
                return jsonify({
                    'success': True,
                    'file': file.read().decode('latin-1')
                }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al comprimir el PDF'
            }), 500
        
    except Exception as e:

        return jsonify({
            'success': False,
            'message': 'Error al comprimir el archivo'
        }), 500
    

@app.route('/word-pdf', methods=['POST'])
def word_a_pdf():
    try:
            file = request.files['file']
            # se guarda el archivo en el directorio de trabajo
            file_path = os.path.join(os.getcwd(), file.filename)
            file.save(file_path)

            pdf_path = convert_word_to_pdf(file_path)
            
            # se elimina el archivo despues de la conversion
            os.remove(file_path)
            
#            if pdf_path:
#                return f"Word convertido: {pdf_path}", 200
#            else:
#                return "Error al convertir el word a PDF", 500
#    except Exception as e:
#        print("Error al convertir el archivo:", e)
#        return "Error al convertir el archivo", 500
            if pdf_path:
                # retornar el archivo convertido
                with open(pdf_path, 'rb') as file:
                    return jsonify({
                        'success': True,
                        'file': file.read().decode('latin-1')
                    }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error al convertir el word a PDF'
                }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al convertir el archivo'
        }), 500





def convert_image_to_pdf(image_file):
    try:
        # se inicializa la herramienta ImageToPdf
        t = ImageToPdf('project_public_f01d038610dc3e7ceb153bcac2563102_srb6q5ff53f3ae552ad94d630786f2aa357a8', verify_ssl=True, proxies=None)

        # se agrega el archivo de imagen
        t.add_file(image_file)

        # se configuran parametros de conversion (opcional)
        t.debug = False
        t.orientation = 'portrait'
        t.margin = 0
        t.pagesize = 'fit'

        # se ejecuta la tarea
        t.execute()

        # se descarga el archivo PDF resultante
        pdf_path = t.download()

        # se elimina la tarea actual
        t.delete_current_task()

        return pdf_path
    except Exception as e:
        print("Error al convertir la imagen a PDF:", e)
        return None


def merge_pdfs(pdf_files):
    try:
        # se inicializa la herramienta Merge
        t = Merge('project_public_f01d038610dc3e7ceb153bcac2563102_srb6q5ff53f3ae552ad94d630786f2aa357a8', verify_ssl=True, proxies=None)

        # se agregan los archivos PDF
        for pdf_file in pdf_files:
            t.add_file(pdf_file)

        # se ejectua la tarea
        t.execute()

        # se descarga el archivo PDF resultante
        pdf_path = t.download()

        # se elimina la tarea actual
        t.delete_current_task()

        return pdf_path
    except Exception as e:
        print("Error al fusionar los archivos PDF:", e)
        return None
    



def compress_pdf(pdf_file):
    try:
        # se inicializa la herramienta Compress
        t = Compress('project_public_f01d038610dc3e7ceb153bcac2563102_srb6q5ff53f3ae552ad94d630786f2aa357a8', verify_ssl=True, proxies=None)

        # se agrega el archivo PDF
        t.add_file(pdf_file)

        # se configuran parametros de compresion (opcional)
        t.debug = False
        t.quality = 'low'
        t.remove_original = False

        # se ejecuta la tarea
        t.execute()

        # se descarga el archivo PDF resultante
        pdf_path = t.download()

        # se elimina la tarea actual
        t.delete_current_task()

        return pdf_path
    except Exception as e:
        print("Error al comprimir el archivo PDF:", e)
        return None
    


def convert_word_to_pdf(word_file):
    try:
        # se inicializa la herramienta OfficeToPdf
        t = OfficeToPdf('project_public_f01d038610dc3e7ceb153bcac2563102_srb6q5ff53f3ae552ad94d630786f2aa357a8', verify_ssl=True, proxies=None)

        # se agrega el archivo de word
        t.add_file(word_file)

        # se configuran parametros de conversion (opcional)
        t.debug = False
        t.orientation = 'portrait'
        t.margin = 0
        t.pagesize = 'fit'

        # se ejecuta la tarea
        t.execute()

        # se descarga el archivo PDF resultante
        pdf_path = t.download()

        # se elimina la tarea actual
        t.delete_current_task()

        return pdf_path
    except Exception as e:
        print("Error al convertir el word a PDF:", e)
        return None



app.run(host="0.0.0.0", port=4000)

