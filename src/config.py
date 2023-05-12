from pathlib import Path

IMAGE_EXTENSIONS = ['*.jpeg', '*.jpg', '*.png']
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(BASE_DIR, 'data')
IMAGE_DIR = Path(DATA_DIR, 'images')
ANNOTATION_DIR = Path(DATA_DIR, 'annotations')
SRC_DIR = Path(BASE_DIR, 'src')
