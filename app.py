from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os
from flask_cors import CORS
from ultralytics import YOLO

# model = YOLO('best.pt')

# app = Flask(__name__, static_url_path='', static_folder='.')
# CORS(app)

# @app.route('/')
# def index_page():
#     return send_from_directory('.', 'index.html')

# @app.route('/style.css')
# def send_css():
#     return send_from_directory('.', 'style.css')

# @app.route('/script.js')
# def send_js():
#     return send_from_directory('.', 'script.js')

# @app.route('/detect', methods=['POST'])
# def detect_wood_sticks():
#     if 'image' not in request.files:
#         print("No image part")  
#         return jsonify({'error': 'ไม่พบไฟล์รูปภาพ'}), 400
    
#     file = request.files['image']
#     if file.filename == '':
#         print("No selected file") 
#         return jsonify({'error': 'ไม่ได้เลือกไฟล์'}), 400

#     try:
        
#         img_np = np.frombuffer(file.read(), np.uint8)
#         img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
#         if img is None:
#             print("Invalid image format")  
#             return jsonify({'error': 'รูปแบบไฟล์ไม่ถูกต้อง'}), 400

#         print("Image loaded successfully")
#         print(f"Image shape: {img.shape}")

       
#         results = model(img, conf=0.5, iou=0.4)[0]  # เพิ่ม confidence threshold
        
#         # กรองเฉพาะ class ที่ต้องการ (ไม้สี)
#         wanted_classes = [0, 1, 2, 3, 4]  
#         detected_objects = []
        
#         if results.boxes is not None:
#             for i, box in enumerate(results.boxes):
#                 class_id = int(box.cls[0])
#                 confidence = float(box.conf[0])
                
#                 # เฉพาะ class ที่ต้องการและมี confidence สูงพอ
#                 if class_id in wanted_classes and confidence > 0.5:
#                     x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    
#                     # วาดกรอบรอบวัตถุที่ตรวจพบ
#                     color_map = {
#                         0: (255, 0, 0),    # blue
#                         1: (0, 255, 0),    # green  
#                         2: (255, 192, 203), # pink
#                         3: (128, 0, 128),   # purple
#                         4: (0, 0, 255)      # red
#                     }
                    
#                     color = color_map.get(class_id, (0, 255, 0))
#                     cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    
#                     # เพิ่มป้ายชื่อ
#                     class_names = ['blue', 'green', 'pink', 'purple', 'red']
#                     label = f"{class_names[class_id]}: {confidence:.2f}"
                    
#                     # วาดพื้นหลังสำหรับข้อความ
#                     (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
#                     cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
                    
#                     # เขียนข้อความ
#                     cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
#                     detected_objects.append({
#                         'class': class_names[class_id],
#                         'confidence': confidence,
#                         'bbox': [x1, y1, x2, y2]
#                     })

#         total_count = len(detected_objects)
        
#         # แปลงภาพที่ตรวจจับแล้วเป็น base64
#         _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
#         img_base64 = base64.b64encode(buffer).decode('utf-8')

#         print(f"Detection completed. Found {total_count} wood sticks")
        
#         # แยกนับตามสี
#         color_counts = {}
#         for obj in detected_objects:
#             color = obj['class']
#             color_counts[color] = color_counts.get(color, 0) + 1

#         return jsonify({
#             'count': total_count,
#             'color_breakdown': color_counts,
#             'detections': detected_objects,
#             'image': img_base64,
#             'message': f'ตรวจพบไม้สี {total_count} ชิ้น'
#         })

#     except Exception as e:
#         print(f"Error during detection: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': f'เกิดข้อผิดพลาดในการประมวลผล: {str(e)}'}), 500

# if __name__ == '__main__':
#     import socket
    
#     # หา IP address ของเครื่อง
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
    
#     print("🚀 Starting Wood Detection Server...")
#     print(f"📡 Local access: http://127.0.0.1:3000")
#     print(f"📱 Mobile/Tablet access: http://{local_ip}:3000")
#     print("📷 Upload images to detect colored wood sticks")
#     print("💡 Make sure all devices are on the same WiFi network")
    
#     app.run(host='0.0.0.0', port=3000, debug=True)