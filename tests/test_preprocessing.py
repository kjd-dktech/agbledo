# ==================================================================
# AgbleDɔ̀_01 - Test unitaire pour la classe DatasetBuilder
#   Focalisé sur :
#    - La nomenclature des fichiers générés
#    - La logique de stratification 70/15/15
# Mantainer: Kodjo Jean DEGBEVI
# ==================================================================

import sys
import pytest
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).parent.parent
test_dir = ROOT_DIR / "tests"
sys.path.append(str(ROOT_DIR))
from src.data.preprocessing import DatasetBuilder

@pytest.fixture
def builder():
    return DatasetBuilder(project_root=test_dir, random_state=42)

def test_format_filename(builder):
    """
    Test la nomenclature des fichiers : {classe_finale}_{source}_{index:05d}.jpg
    """
    filename_ccmt = builder.format_filename("Corn___Fall_Armyworm", "CCMT", 42)
    assert filename_ccmt == "Corn___Fall_Armyworm_CCMT_00042.jpg"
    
    filename_pv = builder.format_filename("Corn___Healthy", "PlantVillage", 1)
    assert filename_pv == "Corn___Healthy_PV_00001.jpg"

def test_stratify_split_ratios(builder):
    """
    Test la logique de stratification 70/15/15.
    """
    # Création d'un dataframe dummy avec des classes déséquilibrées
    data = []
    classes_dist = {
        "Cassava___Mosaic": 1000,
        "Corn___Fall_Armyworm": 200, 
    }
    
    for cls, count in classes_dist.items():
        for _ in range(count):
            data.append({"final_class": cls, "source": "dummy"})
            
    df = pd.DataFrame(data)
    
    df_split = builder.stratify_split(df, train_ratio=0.70, val_ratio=0.15)
    
    assert len(df_split) == 1200
    
    # Vérification globale des proportions
    train_count = len(df_split[df_split['split'] == 'train'])
    val_count = len(df_split[df_split['split'] == 'val'])
    test_count = len(df_split[df_split['split'] == 'test'])
    
    assert abs(train_count - 0.70 * 1200) <= 2 # Tolérance de 2 échantillons
    assert abs(val_count - 0.15 * 1200) <= 2
    assert abs(test_count - 0.15 * 1200) <= 2
    
    # Vérification de la stratification spécifique à la petite classe (Fall Armyworm)
    faw_train = len(df_split[(df_split['final_class'] == 'Corn___Fall_Armyworm') & (df_split['split'] == 'train')])
    assert abs(faw_train - 0.70 * 200) <= 2
