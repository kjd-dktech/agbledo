# ==================================================================
# AgbleDɔ_01 - Préparation des données pour Colab
# Maintainer: Kodjo Jean DEGBEVI
# ==================================================================

from pathlib import Path
from tqdm import tqdm
import os, zipfile, shutil

def prepare_colab_data(PROJECT_ROOT: Path, DATA_DIR: Path):
    """
    Prépare les données pour Colab en créant un zip sur le drive, puis en le copiant et extrayant dans /content.
    - Vérifie que le zip est valide avant de le copier.
    - Vérifie que les fichiers extraits sont identiques à l'original.
    Args:
        PROJECT_ROOT (Path): Racine du projet
        DATA_DIR (Path): Dossier contenant les données à préparer
    """
    # ========= Config =========
    drive_zip = str(PROJECT_ROOT / "data" / "processed.zip")
    colab_zip = "/content/processed.zip"
    COLAB_DATA_DIR = "/content/data"

    # ========= Utils =========
    def zip_valid(zip_path):
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                return z.testzip() is None
        except:
            return False

    def total_size(path):
        return sum(
            os.path.getsize(os.path.join(root, f))
            for root, _, files in os.walk(path)
            for f in files
        )

    # ========= Build zip if needed =========
    if not os.path.exists(drive_zip) or not zip_valid(drive_zip):

        print("\n📦 Création du zip...")

        if os.path.exists(drive_zip):
            os.remove(drive_zip)

        with zipfile.ZipFile(
            drive_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as z:

            for root, _, files in os.walk(str(DATA_DIR)):
                for file in tqdm(files):
                    full = os.path.join(root, file)
                    rel = os.path.relpath(full, str(DATA_DIR))
                    z.write(full, rel)

        if not zip_valid(drive_zip):
            raise Exception("❌ ZIP invalide")

        print("[OK] - ZIP OK")

    else:
        print("\n[OK] - ZIP déjà valide")

    # ========= Copy =========
    print("\n🚚 Copie vers /content...")

    if os.path.exists(colab_zip):
        os.remove(colab_zip)

    shutil.copy2(drive_zip, colab_zip)
    print("[OK] - Copie")

    # ========= Extract =========
    print("\n📂 Extraction...")

    if os.path.exists(COLAB_DATA_DIR):
        shutil.rmtree(COLAB_DATA_DIR)

    os.makedirs(COLAB_DATA_DIR, exist_ok=True)
    with zipfile.ZipFile(colab_zip, "r") as z:
        z.extractall(COLAB_DATA_DIR)

    print("[OK] - Extraction")

    # ========= Verify =========
    print("\n🔎 Vérification...")

    src_count = sum(
        len(files)
        for _, _, files in os.walk(str(DATA_DIR))
    )

    dst_count = sum(
        len(files)
        for _, _, files in os.walk(COLAB_DATA_DIR)
    )

    src_size = total_size(str(DATA_DIR))
    dst_size = total_size(COLAB_DATA_DIR)

    assert src_count == dst_count, "❌ Nombre fichiers différent"
    assert src_size == dst_size, "❌ Taille dataset différente"

    print("[OK] - Vérification")

    # ========= Cleanup =========
    os.remove(colab_zip)
    DATA_DIR = Path(COLAB_DATA_DIR)
    print("\n [OK] - Dataset prêt :", DATA_DIR)