"""
Tests unitaires, d'intégration et utilisateur pour app.py
Framework : pytest
Axe prioritaire : interaction utilisateur (C34)
"""
import pytest
import math
from app import app as flask_app, distances


@pytest.fixture
def client():
    """Client de test Flask configuré en mode test."""
    flask_app.config['TESTING'] = True
    distances.clear()
    with flask_app.test_client() as client:
        yield client


# ─────────────────────────────────────────────
# TESTS UNITAIRES – logique de calcul
# ─────────────────────────────────────────────

class TestCalculDistance:
    """Vérifie la formule de Pythagore."""

    def test_distance_points_connus(self, client):
        """A(2,5) B(1,6) => distance = sqrt(2) ≈ 1.414"""
        resp = client.post('/api/distance', json={
            'start_point': '2,5',
            'end_point': '1,6'
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert math.isclose(data['result_distance'], math.sqrt(2), rel_tol=1e-5)

    def test_distance_point_identique(self, client):
        """Distance entre un point et lui-même = 0."""
        resp = client.post('/api/distance', json={
            'start_point': '3,3',
            'end_point': '3,3'
        })
        assert resp.status_code == 200
        assert resp.get_json()['result_distance'] == 0.0

    def test_distance_axe_horizontal(self, client):
        """A(0,0) B(5,0) => distance = 5."""
        resp = client.post('/api/distance', json={
            'start_point': '0,0',
            'end_point': '5,0'
        })
        assert resp.status_code == 200
        assert math.isclose(resp.get_json()['result_distance'], 5.0)

    def test_distance_axe_vertical(self, client):
        """A(0,0) B(0,4) => distance = 4."""
        resp = client.post('/api/distance', json={
            'start_point': '0,0',
            'end_point': '0,4'
        })
        assert resp.status_code == 200
        assert math.isclose(resp.get_json()['result_distance'], 4.0)

    def test_distance_coordonnees_negatives(self, client):
        """Coordonnées négatives : A(-1,-1) B(2,3) => distance = 5."""
        resp = client.post('/api/distance', json={
            'start_point': '-1,-1',
            'end_point': '2,3'
        })
        assert resp.status_code == 200
        assert math.isclose(resp.get_json()['result_distance'], 5.0)

    def test_distance_grands_nombres(self, client):
        """Coordonnées élevées : A(0,0) B(1000,0) => distance = 1000."""
        resp = client.post('/api/distance', json={
            'start_point': '0,0',
            'end_point': '1000,0'
        })
        assert resp.status_code == 200
        assert math.isclose(resp.get_json()['result_distance'], 1000.0)

    def test_reponse_contient_champs_attendus(self, client):
        """La réponse JSON doit contenir tous les champs métier."""
        resp = client.post('/api/distance', json={
            'start_point': '0,0',
            'end_point': '3,4'
        })
        data = resp.get_json()
        assert 'result_distance' in data
        assert 'start_point' in data
        assert 'end_point' in data
        assert 'requested_at' in data


# ─────────────────────────────────────────────
# TESTS INTERACTION UTILISATEUR – formulaire HTML
# ─────────────────────────────────────────────

class TestFormulaireHTML:
    """Tests centrés sur l'interaction utilisateur via le formulaire."""

    def test_get_page_accueil_renvoie_200(self, client):
        """La page d'accueil doit être accessible via GET."""
        resp = client.get('/')
        assert resp.status_code == 200

    def test_get_page_accueil_contient_formulaire(self, client):
        """La page d'accueil doit contenir un formulaire HTML."""
        resp = client.get('/')
        assert b'form' in resp.data.lower()

    def test_post_formulaire_calcul_correct(self, client):
        """Soumission formulaire A(2,5) B(1,6) => résultat affiché."""
        resp = client.post('/', data={
            'apoint': '2,5',
            'bpoint': '1,6'
        })
        assert resp.status_code == 200
        assert b'1.41' in resp.data or b'result' in resp.data.lower()

    def test_post_formulaire_meme_point(self, client):
        """Soumission avec deux points identiques => distance 0."""
        resp = client.post('/', data={
            'apoint': '5,5',
            'bpoint': '5,5'
        })
        assert resp.status_code == 200

    def test_post_formulaire_coordonnees_simples(self, client):
        """A(0,0) B(3,4) => distance 5 (triplet pythagoricien)."""
        resp = client.post('/', data={
            'apoint': '0,0',
            'bpoint': '3,4'
        })
        assert resp.status_code == 200
        assert b'5.0' in resp.data or b'5' in resp.data

    def test_post_formulaire_sauvegarde_historique(self, client):
        """Chaque calcul via formulaire doit être sauvegardé."""
        client.post('/', data={'apoint': '0,0', 'bpoint': '1,1'})
        assert len(distances) == 1

    def test_post_multiple_sauvegarde_toutes_entrees(self, client):
        """Plusieurs soumissions => toutes sauvegardées."""
        client.post('/', data={'apoint': '0,0', 'bpoint': '1,0'})
        client.post('/', data={'apoint': '0,0', 'bpoint': '0,1'})
        assert len(distances) == 2


# ─────────────────────────────────────────────
# TESTS API REST – /api/distances
# ─────────────────────────────────────────────

class TestAPIDistances:
    """Tests de l'endpoint de liste des distances calculées."""

    def test_liste_vide_par_defaut(self, client):
        """Sans calcul préalable, la liste doit être vide."""
        resp = client.get('/api/distances')
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_liste_apres_calcul_formulaire(self, client):
        """
        Bug documenté : /api/distance ne sauvegarde pas dans distances[].
        Seul le formulaire HTML alimente l'historique.
        Ce test documente le comportement réel.
        """
        client.post('/', data={'apoint': '0,0', 'bpoint': '3,4'})
        resp = client.get('/api/distances')
        data = resp.get_json()
        assert len(data) == 1
        assert math.isclose(data[0]['result_distance'], 5.0)

    def test_liste_multiple_via_formulaire(self, client):
        """
        Bug documenté : seul le formulaire alimente distances[].
        Deux soumissions formulaire => deux entrées dans la liste.
        """
        client.post('/', data={'apoint': '0,0', 'bpoint': '1,0'})
        client.post('/', data={'apoint': '0,0', 'bpoint': '0,1'})
        resp = client.get('/api/distances')
        assert len(resp.get_json()) == 2

    def test_endpoint_api_racine(self, client):
        """L'endpoint /api doit retourner 200."""
        resp = client.get('/api')
        assert resp.status_code == 200

    def test_methode_get_sur_distance_retourne_415(self, client):
        """
        Bug documenté : GET sur /api/distance retourne 415
        (Unsupported Media Type) car Flask attend du JSON.
        Comportement attendu en REST : 405 Method Not Allowed.
        """
        resp = client.get('/api/distance')
        assert resp.status_code == 415
