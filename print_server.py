from flask import Flask, request, jsonify
import cups
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/print', methods=['POST'])
def print_barcode():
    data = request.get_json()
    barcode_image_path = data.get('barcode_image')
    
    if not barcode_image_path:
        logging.error("No barcode image path provided")
        return jsonify({"status": "error", "message": "No barcode image path provided"}), 400
    
    logging.info(f"Received request to print barcode: {barcode_image_path}")
    
    try:
        if not os.path.exists(barcode_image_path):
            logging.error(f"Barcode image file not found: {barcode_image_path}")
            return jsonify({"status": "error", "message": "Barcode image file not found"}), 404

        conn = cups.Connection()
        printers = conn.getPrinters()
        
        if not printers:
            logging.error("No printers found")
            return jsonify({"status": "error", "message": "No printers found"}), 500
        
        printer_name = conn.getDefault()
        if not printer_name:
            logging.error("No default printer set")
            return jsonify({"status": "error", "message": "No default printer set"}), 500
        
        logging.info(f"Using printer: {printer_name}")
        
        print_job_id = conn.printFile(printer_name, barcode_image_path, "Barcode Print", {})
        logging.info(f"Print job created with ID: {print_job_id}")
        
        return jsonify({"status": "success", "message": "Barcode print job created", "print_job_id": print_job_id}), 200
    except Exception as e:
        logging.error(f"Failed to print barcode: {e}")
        return jsonify({"status": "error", "message": "Failed to print barcode"}), 500

if __name__ == '__main__':
    app.run(port=5001)
