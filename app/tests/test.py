import unittest
from app import haversine
class TestHaversine(unittest.TestCase):
    
    def test_zero_distance(self):
        # Mismo punto
        self.assertAlmostEqual(haversine(52.2296756, 21.0122287, 52.2296756, 21.0122287), 0.0, places=6)

    def test_distance_paris_berlin(self):
        # Distancia conocida entre París y Berlín
        # París: 48.8566° N, 2.3522° E
        # Berlín: 52.5200° N, 13.4050° E
        distance = haversine(48.8566, 2.3522, 52.5200, 13.4050)
        self.assertAlmostEqual(distance, 878.0, delta=1.0)  # Distancia esperada en km

    def test_distance_london_new_york(self):
        # Distancia conocida entre Londres y Nueva York
        # Londres: 51.5074° N, 0.1278° W
        # Nueva York: 40.7128° N, 74.0060° W
        distance = haversine(51.5074, -0.1278, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 5570.0, delta=10.0)  # Distancia esperada en km

    def test_distance_equator(self):
        # Distancia a lo largo del ecuador
        # Quito (Ecuador): 0.0° N, 78.5° W
        # Ciudad de México: 19.4326° N, 99.1332° W
        distance = haversine(0.0, -78.5, 19.4326, -99.1332)
        self.assertAlmostEqual(distance, 3894.0, delta=20.0)  # Distancia esperada en km

    def test_invalid_coordinates(self):
        # Probar con coordenadas inválidas
        with self.assertRaises(ValueError):
            haversine(100, 200, -100, -200)  # Coordenadas fuera de rango

if __name__ == '__main__':
    unittest.main()
