# ==================================================================
# AgbleDɔ_01 - Prétraitement des données
# Maintainer: Kodjo Jean DEGBEVI
# ==================================================================

import sys
from pathlib import Path
import pandas as pd
import shutil
from PIL import Image
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from src.data.utils import class_name_mapping

class DatasetBuilder:
    """
    Classe responsable de la construction du dataset processed.
    Règles de nettoyage, de renommage et le split stratifié.
    """
    
    def __init__(self, project_root: Path, random_state: int = 42):
        self.project_root = Path(project_root)
        self.raw_dir = self.project_root / "data" / "raw"
        self.processed_dir = self.project_root / "data" / "processed"
        self.logs_dir = self.project_root / "logs" / "preprocessing"
        self.random_state = random_state
        self.class_mapping = class_name_mapping()
        
    def _read_corrupted_list(self) -> set:
        corrupted_file = self.logs_dir / "corrupted_images.txt"
        if corrupted_file.exists():
            with open(corrupted_file, "r") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def get_valid_files_df(self) -> pd.DataFrame:
        """
        Parcourt data/raw et retourne un DataFrame des images valides
        avec leurs classes finales et sources.
        """
        corrupted_paths = self._read_corrupted_list()
        records = []
        
        for file_path in self.raw_dir.rglob('*'):
            if not file_path.is_file():
                continue
                
            rel_path_str = str(file_path.relative_to(self.project_root))
            
            if rel_path_str in corrupted_paths or "x_Removed" in rel_path_str:
                continue
                
            parts = file_path.relative_to(self.raw_dir).parts
            if len(parts) >= 3:
                source = parts[0]
                crop = parts[1]
                orig_class = parts[2]
                
                mapping_key = f"{source}/{crop}/{orig_class}"
                final_class = self.class_mapping.get(mapping_key, "Unknown")
                
                if final_class != "Unknown":
                    records.append({
                        "original_filepath": rel_path_str,
                        "abs_path": file_path,
                        "final_class": final_class,
                        "source": source
                    })
                    
        return pd.DataFrame(records)

    def stratify_split(self, df: pd.DataFrame, train_ratio=0.70, val_ratio=0.15) -> pd.DataFrame:
        """
        Réalise un split stratifié 70/15/15.
        """
        # Train / Temp
        train_df, temp_df = train_test_split(
            df, 
            test_size=(1.0 - train_ratio), 
            stratify=df['final_class'], 
            random_state=self.random_state
        )
        
        # Val / Test
        relative_val_ratio = val_ratio / (1.0 - train_ratio)
        val_df, test_df = train_test_split(
            temp_df, 
            test_size=(1.0 - relative_val_ratio), 
            stratify=temp_df['final_class'], 
            random_state=self.random_state
        )
        
        train_df['split'] = 'train'
        val_df['split'] = 'val'
        test_df['split'] = 'test'
        
        return pd.concat([train_df, val_df, test_df])

    def format_filename(self, final_class: str, source: str, index: int) -> str:
        """
        Génère le nom de fichier conventionné.
        """
        source_code = "PV" if source == "PlantVillage" else "CCMT"
        return f"{final_class}_{source_code}_{index:05d}.jpg"

    def build_dataset(self):
        """
        Exécute le pipeline entier.
        """
        print("1. Récupération des fichiers valides...")
        df = self.get_valid_files_df()
        
        print("2. Exécution du split stratifié (70/15/15)...")
        df = self.stratify_split(df)
        
        print("3. Préparation des répertoires...")
        if self.processed_dir.exists():
            shutil.rmtree(self.processed_dir)
            
        splits = ['train', 'val', 'test']
        classes = df['final_class'].unique()
        
        for split in splits:
            for cls in classes:
                (self.processed_dir / split / cls).mkdir(parents=True, exist_ok=True)
                
        print("4. Traitement et copie des images...")
        summary_records = []
        
        class_counters = {cls: 1 for cls in classes}

        conversions_log_path = self.logs_dir / "extension_conversions.txt"
        conversions = []
        
        for _, row in tqdm(df.iterrows(), total=len(df)):
            final_class = row['final_class']
            source = row['source']
            split = row['split']
            orig_abs_path = row['abs_path']
            
            # Nouvelle numérotation
            idx = class_counters[final_class]
            class_counters[final_class] += 1
            
            # Nouveau nom
            new_filename = self.format_filename(final_class, source, idx)
            new_rel_path = f"data/processed/{split}/{final_class}/{new_filename}"
            new_abs_path = self.project_root / new_rel_path
            
            # Copie et conversion éventuelle si non jpg standard
            if orig_abs_path.suffix.lower() not in ['.jpg', '.jpeg']:
                conversions.append(f"{row['original_filepath']} -> {new_rel_path}")
                # Conversion via PIL
                with Image.open(orig_abs_path) as img:
                    rgb_im = img.convert('RGB')
                    rgb_im.save(new_abs_path, 'JPEG', quality=95)
            else:
                shutil.copy2(orig_abs_path, new_abs_path)
                
            summary_records.append({
                "filepath": new_rel_path,
                "class": final_class,
                "source": "PV" if source == "PlantVillage" else source,
                "split": split
            })
            
        # Log des conversions
        if conversions:
            with open(conversions_log_path, "w") as f:
                f.write("\n".join(conversions))
                
        print("5. Génération du data_summary.csv...")
        summary_df = pd.DataFrame(summary_records)
        summary_csv_path = self.processed_dir / "data_summary.csv"
        summary_df.to_csv(summary_csv_path, index=False)
        
        print("Pipeline de prétraitement terminé avec succès ! ✅")
        return summary_df
