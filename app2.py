from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import torch  # Pour charger les modèles de classification

app = Flask(__name__)
CORS(app)

# Charger les modèles
model_yolo = YOLO('weights/best.pt')  # YOLOv8 pour la détection
model_class_dorsale = torch.load('weights/male_femelle_classification.h5')  # Modèle pour classification dorsale
model_class_ventrale = torch.load('weights/male_femelle_classification.h5')  # Modèle pour classification ventrale

# Mettre les modèles en mode évaluation
model_class_dorsale.eval()
model_class_ventrale.eval()

@app.route('/predict', methods=['POST'])
def predict():
    # Vérifier si une image est fournie dans la requête
    if 'image' not in request.files:
        return jsonify({"error": "Pas d'image trouvée dans la requête"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400
    
    img = Image.open(file.stream)  # Ouvrir l'image avec PIL

    # Étape 1 : Faire l'inférence avec YOLOv8 (pour détection et prédiction de la face)
    results = model_yolo(img)
    if len(results[0].boxes.data) == 0:
        return jsonify({"error": "Aucune tique détectée"}), 200

    # Extraire les coordonnées de la première boîte (x1, y1, x2, y2) et la prédiction de la face
    box = results[0].boxes.data[0].tolist()[:4]
    class_id = int(results[0].boxes.data[0][5])  # 0 = dorsale, 1 = ventrale
    x1, y1, x2, y2 = map(int, box)

    # Recadrer l'image de la tique détectée
    cropped_img = img.crop((x1, y1, x2, y2))

    # Convertir l'image recadrée en tensor pour le modèle de classification
    cropped_img_tensor = transform_image_to_tensor(cropped_img)

    # Étape 2 : Déterminer le type de classification en fonction de la face (dorsale ou ventrale)
    if class_id == 0:  # Face dorsale
        classification_output = model_class_dorsale(cropped_img_tensor)
        predicted_class = torch.argmax(classification_output).item()
        classification = "dorsale"
    else:  # Face ventrale
        classification_output = model_class_ventrale(cropped_img_tensor)
        predicted_class = torch.argmax(classification_output).item()
        classification = "ventrale"

    # Construire la réponse JSON avec la face et la classification prédite
    response = {
        "face": classification,  
        "classification_result": predicted_class 
    }

    return jsonify(response), 200

def transform_image_to_tensor(image):
    
    from torchvision import transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0) 

if __name__ == '__main__':
    app.run(debug=True)
