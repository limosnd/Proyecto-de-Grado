"""
Script para evaluar el modelo de Hugging Face con métricas de rendimiento
Incluye accuracy, precision, recall, F1-score, matriz de confusión y más
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
from huggingface_hub import hf_hub_download
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
import os
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class BIRADSModelEvaluator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = None
        self.class_names = ['BI-RADS 1', 'BI-RADS 2', 'BI-RADS 3', 'BI-RADS 4', 'BI-RADS 5']
        self.repo_id = "Enterwar99/MODEL_MAMMOGRAFII"
        self.filename = "best_model.pth"
        
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
        print("🔄 Descargando modelo desde Hugging Face...")
        try:
            model_path = hf_hub_download(repo_id=self.repo_id, filename=self.filename)
            self.model = self.get_model_architecture()
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print("✅ Modelo cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def predict_single_image(self, image_path):
        """Predecir una sola imagen"""
        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probs = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probs, 1)
                
                return {
                    'predicted_class': predicted_idx.item(),
                    'confidence': float(confidence),
                    'probabilities': probs.squeeze().cpu().numpy()
                }
        except Exception as e:
            print(f"❌ Error procesando imagen {image_path}: {e}")
            return None
    
    def evaluate_dataset(self, test_data_path, ground_truth_file=None):
        """
        Evaluar el modelo en un dataset de prueba
        
        Args:
            test_data_path: Ruta al directorio con imágenes de prueba
            ground_truth_file: Archivo JSON con las etiquetas verdaderas
                               Formato: {"imagen.jpg": clase_verdadera, ...}
        """
        print("🔄 Iniciando evaluación del dataset...")
        
        # Si no hay archivo de ground truth, crear uno interactivo
        if ground_truth_file is None or not os.path.exists(ground_truth_file):
            print("📝 No se encontró archivo de ground truth. Creando uno nuevo...")
            ground_truth = self.create_ground_truth_file(test_data_path)
        else:
            with open(ground_truth_file, 'r') as f:
                ground_truth = json.load(f)
        
        predictions = []
        true_labels = []
        probabilities = []
        image_names = []
        
        # Procesar cada imagen
        for image_name, true_label in ground_truth.items():
            image_path = os.path.join(test_data_path, image_name)
            if os.path.exists(image_path):
                result = self.predict_single_image(image_path)
                if result:
                    predictions.append(result['predicted_class'])
                    true_labels.append(true_label)
                    probabilities.append(result['probabilities'])
                    image_names.append(image_name)
                    
                    print(f"✅ {image_name}: Predicho={result['predicted_class']+1}, Real={true_label+1}, Confianza={result['confidence']:.3f}")
        
        if not predictions:
            print("❌ No se pudieron procesar imágenes")
            return None
        
        # Calcular métricas
        metrics = self.calculate_metrics(true_labels, predictions, probabilities)
        
        # Crear visualizaciones
        self.create_visualizations(true_labels, predictions, probabilities, metrics)
        
        # Crear reporte detallado
        self.create_detailed_report(true_labels, predictions, image_names, metrics)
        
        return metrics
    
    def create_ground_truth_file(self, test_data_path):
        """Crear archivo de ground truth interactivamente"""
        ground_truth = {}
        image_files = [f for f in os.listdir(test_data_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.dcm'))]
        
        print(f"\n📋 Encontradas {len(image_files)} imágenes para etiquetar")
        print("Ingresa la clase BI-RADS verdadera para cada imagen (1-5):")
        
        for i, image_file in enumerate(image_files, 1):
            print(f"\n🖼️  Imagen {i}/{len(image_files)}: {image_file}")
            while True:
                try:
                    birads = int(input("Clase BI-RADS (1-5): "))
                    if 1 <= birads <= 5:
                        ground_truth[image_file] = birads - 1  # Convertir a índice 0-4
                        break
                    else:
                        print("❌ Ingresa un número entre 1 y 5")
                except ValueError:
                    print("❌ Ingresa un número válido")
        
        # Guardar archivo
        gt_file = os.path.join(test_data_path, 'ground_truth.json')
        with open(gt_file, 'w') as f:
            json.dump(ground_truth, f, indent=2)
        
        print(f"💾 Ground truth guardado en: {gt_file}")
        return ground_truth
    
    def calculate_metrics(self, true_labels, predictions, probabilities):
        """Calcular todas las métricas de evaluación"""
        metrics = {}
        
        # Métricas básicas
        metrics['accuracy'] = accuracy_score(true_labels, predictions)
        metrics['precision_macro'] = precision_score(true_labels, predictions, average='macro', zero_division=0)
        metrics['recall_macro'] = recall_score(true_labels, predictions, average='macro', zero_division=0)
        metrics['f1_macro'] = f1_score(true_labels, predictions, average='macro', zero_division=0)
        
        # Métricas por clase
        metrics['precision_per_class'] = precision_score(true_labels, predictions, average=None, zero_division=0)
        metrics['recall_per_class'] = recall_score(true_labels, predictions, average=None, zero_division=0)
        metrics['f1_per_class'] = f1_score(true_labels, predictions, average=None, zero_division=0)
        
        # Matriz de confusión
        metrics['confusion_matrix'] = confusion_matrix(true_labels, predictions)
        
        # Reporte de clasificación
        metrics['classification_report'] = classification_report(
            true_labels, predictions, 
            target_names=self.class_names,
            output_dict=True
        )
        
        # Calcular AUC para clasificación multiclase
        if len(set(true_labels)) > 2:  # Multiclase
            try:
                true_labels_bin = label_binarize(true_labels, classes=list(range(5)))
                probabilities_array = np.array(probabilities)
                
                metrics['auc_per_class'] = {}
                for i in range(5):
                    if np.sum(true_labels_bin[:, i]) > 0:  # Solo si hay ejemplos de esta clase
                        fpr, tpr, _ = roc_curve(true_labels_bin[:, i], probabilities_array[:, i])
                        metrics['auc_per_class'][f'BI-RADS {i+1}'] = auc(fpr, tpr)
            except Exception as e:
                print(f"⚠️ No se pudo calcular AUC: {e}")
                metrics['auc_per_class'] = {}
        
        return metrics
    
    def create_visualizations(self, true_labels, predictions, probabilities, metrics):
        """Crear visualizaciones de los resultados"""
        # Configurar matplotlib
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Matriz de confusión
        cm = metrics['confusion_matrix']
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.class_names, yticklabels=self.class_names,
                   ax=axes[0,0])
        axes[0,0].set_title('Matriz de Confusión')
        axes[0,0].set_xlabel('Predicción')
        axes[0,0].set_ylabel('Verdadero')
        
        # 2. Métricas por clase
        classes = [f'BI-RADS {i+1}' for i in range(5)]
        x_pos = np.arange(len(classes))
        
        axes[0,1].bar(x_pos - 0.2, metrics['precision_per_class'], 0.2, label='Precision', alpha=0.8)
        axes[0,1].bar(x_pos, metrics['recall_per_class'], 0.2, label='Recall', alpha=0.8)
        axes[0,1].bar(x_pos + 0.2, metrics['f1_per_class'], 0.2, label='F1-Score', alpha=0.8)
        axes[0,1].set_xlabel('Clases BI-RADS')
        axes[0,1].set_ylabel('Score')
        axes[0,1].set_title('Métricas por Clase')
        axes[0,1].set_xticks(x_pos)
        axes[0,1].set_xticklabels(classes)
        axes[0,1].legend()
        axes[0,1].set_ylim(0, 1.1)
        
        # 3. Distribución de predicciones vs verdaderas
        prediction_counts = np.bincount(predictions, minlength=5)
        true_counts = np.bincount(true_labels, minlength=5)
        
        x_pos = np.arange(5)
        axes[1,0].bar(x_pos - 0.2, true_counts, 0.4, label='Etiquetas Verdaderas', alpha=0.8)
        axes[1,0].bar(x_pos + 0.2, prediction_counts, 0.4, label='Predicciones', alpha=0.8)
        axes[1,0].set_xlabel('Clases BI-RADS')
        axes[1,0].set_ylabel('Cantidad')
        axes[1,0].set_title('Distribución de Clases')
        axes[1,0].set_xticks(x_pos)
        axes[1,0].set_xticklabels([f'BI-RADS {i+1}' for i in range(5)])
        axes[1,0].legend()
        
        # 4. Resumen de métricas principales
        axes[1,1].axis('off')
        metrics_text = f"""
        RESUMEN DE MÉTRICAS
        
        Accuracy: {metrics['accuracy']:.3f}
        Precision (Macro): {metrics['precision_macro']:.3f}
        Recall (Macro): {metrics['recall_macro']:.3f}
        F1-Score (Macro): {metrics['f1_macro']:.3f}
        
        Total de imágenes: {len(true_labels)}
        Total de clases: {len(set(true_labels))}
        """
        axes[1,1].text(0.1, 0.5, metrics_text, fontsize=12, 
                      verticalalignment='center', 
                      bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        plt.tight_layout()
        plt.savefig('model_evaluation_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("📊 Visualizaciones guardadas en 'model_evaluation_results.png'")
    
    def create_detailed_report(self, true_labels, predictions, image_names, metrics):
        """Crear reporte detallado en formato CSV y texto"""
        
        # Reporte por imagen
        results_df = pd.DataFrame({
            'Imagen': image_names,
            'Etiqueta_Verdadera': [f'BI-RADS {label+1}' for label in true_labels],
            'Prediccion': [f'BI-RADS {pred+1}' for pred in predictions],
            'Correcto': [true == pred for true, pred in zip(true_labels, predictions)]
        })
        
        results_df.to_csv('detailed_predictions.csv', index=False)
        print("📄 Predicciones detalladas guardadas en 'detailed_predictions.csv'")
        
        # Reporte de texto
        with open('evaluation_report.txt', 'w', encoding='utf-8') as f:
            f.write("=== REPORTE DE EVALUACIÓN DEL MODELO BI-RADS ===\n\n")
            f.write(f"Modelo: {self.repo_id}\n")
            f.write(f"Fecha de evaluación: {pd.Timestamp.now()}\n")
            f.write(f"Dispositivo: {self.device}\n\n")
            
            f.write("=== MÉTRICAS GENERALES ===\n")
            f.write(f"Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"Precision (Macro): {metrics['precision_macro']:.4f}\n")
            f.write(f"Recall (Macro): {metrics['recall_macro']:.4f}\n")
            f.write(f"F1-Score (Macro): {metrics['f1_macro']:.4f}\n\n")
            
            f.write("=== MÉTRICAS POR CLASE ===\n")
            for i, class_name in enumerate(self.class_names):
                f.write(f"{class_name}:\n")
                f.write(f"  Precision: {metrics['precision_per_class'][i]:.4f}\n")
                f.write(f"  Recall: {metrics['recall_per_class'][i]:.4f}\n")
                f.write(f"  F1-Score: {metrics['f1_per_class'][i]:.4f}\n")
                if 'auc_per_class' in metrics and class_name in metrics['auc_per_class']:
                    f.write(f"  AUC: {metrics['auc_per_class'][class_name]:.4f}\n")
                f.write("\n")
            
            f.write("=== MATRIZ DE CONFUSIÓN ===\n")
            f.write("Filas = Etiquetas verdaderas, Columnas = Predicciones\n")
            f.write("     " + "  ".join([f"B{i+1}" for i in range(5)]) + "\n")
            for i, row in enumerate(metrics['confusion_matrix']):
                f.write(f"B{i+1}: " + "  ".join([f"{val:3d}" for val in row]) + "\n")
            
            f.write(f"\n=== RESUMEN ===\n")
            f.write(f"Total de imágenes evaluadas: {len(true_labels)}\n")
            f.write(f"Predicciones correctas: {sum(true_labels[i] == predictions[i] for i in range(len(true_labels)))}\n")
            f.write(f"Predicciones incorrectas: {sum(true_labels[i] != predictions[i] for i in range(len(true_labels)))}\n")
        
        print("📄 Reporte completo guardado en 'evaluation_report.txt'")

def main():
    """Función principal para ejecutar la evaluación"""
    print("🚀 Iniciando evaluación del modelo BI-RADS")
    
    # Crear evaluador
    evaluator = BIRADSModelEvaluator()
    
    # Configurar rutas (ajustar según tu estructura)
    test_data_path = input("📁 Ingresa la ruta al directorio con imágenes de prueba: ").strip()
    
    if not os.path.exists(test_data_path):
        print("❌ La ruta no existe")
        return
    
    ground_truth_file = os.path.join(test_data_path, 'ground_truth.json')
    
    # Ejecutar evaluación
    metrics = evaluator.evaluate_dataset(test_data_path, ground_truth_file)
    
    if metrics:
        print("\n🎉 Evaluación completada exitosamente!")
        print(f"📊 Accuracy: {metrics['accuracy']:.3f}")
        print(f"📊 F1-Score (Macro): {metrics['f1_macro']:.3f}")
        print("📁 Revisa los archivos generados para más detalles")
    else:
        print("❌ Error en la evaluación")

if __name__ == "__main__":
    main()