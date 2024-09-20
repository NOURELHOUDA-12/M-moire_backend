# import argparse
# import io
# from PIL import Image
# import datetime
# import torch
# import cv2
# import numpy as np
# import tensorflow as tf
# from flask import Flask, render_template, request, redirect, send_file, url_for, Response
# from werkzeug.utils import secure_filename, send_from_directory
# import os
# import subprocess
# import re
# import requests
# import shutil
# import time
# import glob
# from ultralytics import YOLO

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return render_template("./index.html")

# @app.route("/", methods=["GET", "POST"])
# def predict_img():
#     if request.method == "POST":
#         if 'file' in request.files:
#             f = request.files['file']
#             basePath = os.path.dirname(__file__)
#             filePath = os.path.join(basePath, 'uploads', secure_filename(f.filename))
#             print("Upload folder is ", filePath)
#             f.save(filePath)
            
#             file_extension = os.path.splitext(f.filename)[1].lower()

#             if file_extension == '.jpg':
#                 img = cv2.imread(filePath)
#                 frame = cv2.imencode('.jpg', img)[1].tobytes()

#                 image = Image.open(io.BytesIO(frame))

#                 # Initialisation du modèle YOLO
#                 yolo = YOLO('best.pt')  # Assure-toi que ton modèle est correct
                
#                 # Détection avec sauvegarde forcée
#                 detections = yolo.predict(image, save=True, save_dir=os.path.join(os.getcwd(), 'runs/detect/predict9'))
#                 for detection in detections:
#                     print("Résultat de la détection YOLO :", detection)
#                     if detections:
#                         print(f"Nombre de détections : {len(detections)}")
#                     else:
#                         print("Aucune détection n'a été effectuée.")
#                 # Débogage des résultats
#                 print("Détections YOLO :", detections)

#                 if detections:
#                     save_dir = detections[0].save_dir
#                     print("Dossier de sauvegarde :", save_dir)
                    
#                     # Vérifier les fichiers dans le dossier de sauvegarde
#                     if os.path.exists(save_dir):
#                         files_in_save_dir = os.listdir(save_dir)
#                         print("Fichiers dans le dossier de sauvegarde :", files_in_save_dir)
#                     else:
#                         print("Le dossier de sauvegarde n'existe pas.")
#                 else:
#                     print("Aucune détection n'a été trouvée par YOLO.")

#                 return display(f.filename)

#             elif file_extension == '.mp4':
#                 videoPath = filePath
#                 cap = cv2.VideoCapture(videoPath)

#                 # Obtenir les dimensions de la vidéo
#                 frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                 frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#                 # Définir le codec et créer l'objet VideoWriter
#                 fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#                 out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

#                 # Initialiser le modèle YOLOv8 ici
#                 model = YOLO('best.pt')

#                 while cap.isOpened():
#                     ret, frame = cap.read()
#                     if not ret:
#                         break
                    
#                     # YOLOv8 détection
#                     results = model(frame, save=True)
#                     res_plotted = results[0].plot()

#                     # Écrire la trame dans la vidéo de sortie
#                     out.write(res_plotted)

#                 return video_feed()

#     return render_template("index.html")

# def get_frame():
#     video = cv2.VideoCapture('output.mp4')
#     while True:
#         success, image = video.read()
#         if not success:
#             break
#         ret, jpeg = cv2.imencode('.jpg', image)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
#         time.sleep(0.1)

# @app.route("/video_feed")
# def video_feed():
#     return Response(get_frame(), mimetype='multipart/x-mixed-replace;boundary=frame')

# @app.route('/<path:filename>')
# def display(filename):
#     folderPath = 'runs/detect'
#     subfolders = [f for f in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, f))]
    
#     if not subfolders:
#         return "Aucun sous-dossier trouvé dans le dossier des détections."

#     latest_subFolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folderPath, x)))
#     directory = os.path.join(folderPath, latest_subFolder)
    
#     print("Dossier sélectionné:", directory)
    
#     files = os.listdir(directory)
#     if not files:
#         return "Aucun fichier trouvé dans le dossier de détection."
    
#     latest_file = files[0]
#     file_extension = os.path.splitext(latest_file)[1].lower()

#     if file_extension == '.jpg':
#         return send_from_directory(directory, latest_file)
#     else:
#         return 'Format de fichier non valide'

# if __name__ == "__main__":
#     app.run(debug=True, port=9000)
