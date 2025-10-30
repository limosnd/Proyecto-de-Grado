"""
Script simplificado para pruebas rápidas del modelo
Úsalo cuando quieras evaluar pocas imágenes rápidamente
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
from huggingface_hub import hf_hub_download
import numpy as np
import os
from pathlib import Path

class QuickModelTester:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = None
        self.class_names = ['BI-RADS 1', 'BI-RADS 2', 'BI-RADS 3', 'BI-RADS 4', 'BI-RADS 5']
        
        # Configurar transformaciones
        imagenet_mean = [0.485, 0.456, 0.406]
        imagenet_std = [0.229, 0.224, 0.225]
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std)
        ])
        
        self.load_model()
    
    def get_model_architecture(self):
        """Crear la arquitectura del modelo"""
        model = models.resnet18(weights=None)
        num_feats = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_feats, 5)
        )
        return model
    
    def load_model(self):
        """Cargar el modelo desde Hugging Face"""
        print("🔄 Cargando modelo...")
        try:
            model_path = hf_hub_download(repo_id="Enterwar99/MODEL_MAMMOGRAFII", filename="best_model.pth")
            self.model = self.get_model_architecture()
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print(f"✅ Modelo cargado en {self.device}")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def test_single_image(self, image_path, true_label=None):
        """Probar una sola imagen"""
        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probs = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probs, 1)
                
                predicted_class = predicted_idx.item()
                confidence_score = float(confidence)
                probabilities = probs.squeeze().cpu().numpy()
                
                print(f"\n🖼️  Imagen: {os.path.basename(image_path)}")
                print(f"🎯 Predicción: {self.class_names[predicted_class]} (Clase {predicted_class + 1})")
                print(f"🎲 Confianza: {confidence_score:.3f} ({confidence_score*100:.1f}%)")
                
                if true_label is not None:
                    true_idx = true_label - 1  # Convertir de 1-5 a 0-4
                    correct = "✅" if predicted_class == true_idx else "❌"
                    print(f"📋 Etiqueta real: {self.class_names[true_idx]} (Clase {true_label})")
                    print(f"🎯 Resultado: {correct}")
                
                print("📊 Probabilidades por clase:")
                for i, (class_name, prob) in enumerate(zip(self.class_names, probabilities)):
                    bar = "█" * int(prob * 20)  # Barra visual
                    print(f"   {class_name}: {prob:.3f} ({prob*100:5.1f}%) {bar}")
                
                return {
                    'predicted_class': predicted_class,
                    'predicted_birads': predicted_class + 1,
                    'confidence': confidence_score,
                    'probabilities': probabilities.tolist(),
                    'correct': predicted_class == (true_label - 1) if true_label else None
                }
                
        except Exception as e:
            print(f"❌ Error procesando imagen: {e}")
            return None
    
    def test_directory(self, directory_path, ask_for_labels=True):
        """Probar todas las imágenes en un directorio"""
        image_extensions = ('.png', '.jpg', '.jpeg', '.dcm', '.tif', '.tiff')
        image_files = [f for f in os.listdir(directory_path) 
                      if f.lower().endswith(image_extensions)]
        
        if not image_files:
            print("❌ No se encontraron imágenes en el directorio")
            return
        
        print(f"📁 Encontradas {len(image_files)} imágenes")
        results = []
        correct_predictions = 0
        total_predictions = 0
        
        for image_file in image_files:
            image_path = os.path.join(directory_path, image_file)
            
            true_label = None
            if ask_for_labels:
                while True:
                    try:
                        user_input = input(f"\n¿Cuál es la etiqueta real para {image_file}? (1-5, o 's' para saltar): ")
                        if user_input.lower() == 's':
                            break
                        true_label = int(user_input)
                        if 1 <= true_label <= 5:
                            break
                        else:
                            print("❌ Ingresa un número entre 1 y 5")
                    except ValueError:
                        print("❌ Ingresa un número válido o 's' para saltar")
            
            result = self.test_single_image(image_path, true_label)
            if result:
                results.append(result)
                if result['correct'] is not None:
                    total_predictions += 1
                    if result['correct']:
                        correct_predictions += 1
        
        # Resumen
        if total_predictions > 0:
            accuracy = correct_predictions / total_predictions
            print(f"\n📈 RESUMEN:")
            print(f"🎯 Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
            print(f"✅ Correctas: {correct_predictions}/{total_predictions}")
            print(f"❌ Incorrectas: {total_predictions - correct_predictions}/{total_predictions}")
        
        return results
    
    def quick_test(self):
        """Modo de prueba rápida interactivo"""
        print("🚀 Modo de prueba rápida del modelo BI-RADS")
        print("Opciones:")
        print("1. Probar una imagen")
        print("2. Probar un directorio")
        print("3. Salir")
        
        while True:
            choice = input("\n🔢 Elige una opción (1-3): ")
            
            if choice == "1":
                image_path = input("📁 Ruta de la imagen: ").strip()
                if os.path.exists(image_path):
                    true_label = None
                    ask_label = input("¿Conoces la etiqueta real? (y/n): ").lower()
                    if ask_label == 'y':
                        while True:
                            try:
                                true_label = int(input("Etiqueta real (1-5): "))
                                if 1 <= true_label <= 5:
                                    break
                                else:
                                    print("❌ Ingresa un número entre 1 y 5")
                            except ValueError:
                                print("❌ Ingresa un número válido")
                    
                    self.test_single_image(image_path, true_label)
                else:
                    print("❌ Archivo no encontrado")
            
            elif choice == "2":
                directory_path = input("📁 Ruta del directorio: ").strip()
                if os.path.exists(directory_path):
                    ask_labels = input("¿Quieres ingresar etiquetas reales para calcular accuracy? (y/n): ").lower() == 'y'
                    self.test_directory(directory_path, ask_labels)
                else:
                    print("❌ Directorio no encontrado")
            
            elif choice == "3":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")

def main():
    """Función principal"""
    tester = QuickModelTester()
    tester.quick_test()

if __name__ == "__main__":
    main()