from pathlib import Path

import cv2
import numpy as np
import pytest

from dbmdofus.ocr import Lecture, MoteurAucun, detecter_motif, preparer

FIXTURES = Path(__file__).parent / "fixtures"


def _image_avec_texte(texte: str) -> np.ndarray:
    img = np.zeros((60, 200, 3), np.uint8)
    cv2.putText(img, texte, (10, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    return img


def test_lecture_nombre():
    assert Lecture("Tour 12", 0.9).nombre() == 12
    assert Lecture("", 0.0).nombre() is None


def test_moteur_aucun():
    m = MoteurAucun()
    assert not m.disponible and m.lire(_image_avec_texte("3")).confiance == 0.0


def test_preparer_binarise():
    out = preparer(_image_avec_texte("7"))
    assert out.shape == (120, 400) and set(np.unique(out)) <= {0, 255}


def test_detecter_motif():
    img = _image_avec_texte("TOUR")
    motif = img[15:50, 5:80].copy()
    assert detecter_motif(img, motif).confiance > 0.95
    assert detecter_motif(_image_avec_texte("xx"), motif).confiance < 0.9


@pytest.mark.skipif(not any(FIXTURES.glob("*.png")), reason="pas encore de captures de test")
def test_fixtures_lisibles():
    for f in FIXTURES.glob("*.png"):
        assert cv2.imread(str(f)) is not None
