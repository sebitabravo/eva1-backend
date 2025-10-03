"""
Tests de seguridad para drfmaderas.

Verifica que las medidas de seguridad funcionen correctamente.
"""
from django.test import TestCase, Client, override_settings
from django.urls import reverse


class SecurityTests(TestCase):
    """Tests de seguridad para URLs y vistas."""

    def setUp(self):
        """Configurar cliente de prueba."""
        self.client = Client()

    def test_root_redirects_to_api(self):
        """
        Test: La URL raíz (/) debe redirigir a /api/
        Esto previene exponer rutas en página 404.
        """
        response = self.client.get('/')

        # Verificar redirección permanente (301)
        self.assertEqual(response.status_code, 301)

        # Verificar que redirige a /api/
        self.assertEqual(response.url, '/api/')

    def test_root_redirect_is_permanent(self):
        """
        Test: La redirección debe ser permanente (301) no temporal (302).
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)  # 301 = Permanent, 302 = Temporary

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_custom_404_handler_in_production(self):
        """
        Test: Con DEBUG=False, las URLs inexistentes deben retornar
        la vista personalizada sin revelar información.
        """
        response = self.client.get('/ruta-inexistente/')

        # Verificar que retorna 404
        self.assertEqual(response.status_code, 404)

        # Verificar que NO es la página de debug de Django
        # (la página de debug contiene "Using the URLconf defined in")
        self.assertNotContains(
            response,
            'Using the URLconf defined in',
            status_code=404
        )

    def test_admin_url_is_accessible(self):
        """
        Test: La URL de admin debe ser accesible.
        """
        response = self.client.get('/admin/')

        # Debe redirigir al login (302) o mostrar la página (200)
        # dependiendo si hay sesión activa
        self.assertIn(response.status_code, [200, 302])

    def test_api_url_is_accessible(self):
        """
        Test: La URL de API debe ser accesible.
        """
        response = self.client.get('/api/')

        # Debe retornar 200 OK
        self.assertEqual(response.status_code, 200)


class SecurityHeadersTests(TestCase):
    """Tests para verificar headers de seguridad."""

    def setUp(self):
        """Configurar cliente de prueba."""
        self.client = Client()

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_security_headers_in_production(self):
        """
        Test: Con DEBUG=False, los headers de seguridad deben estar presentes.
        Nota: Algunos headers solo se añaden por middleware en producción.
        """
        response = self.client.get('/api/')

        # Verificar X-Frame-Options (previene clickjacking)
        # Este header debería estar presente con DEBUG=False
        # Django lo añade automáticamente con el middleware de seguridad
        self.assertTrue(
            'X-Frame-Options' in response or
            'X-Content-Type-Options' in response,
            "Los headers de seguridad deben estar presentes en producción"
        )


class AdminURLConfigTests(TestCase):
    """Tests para verificar configuración de URL de admin."""

    def test_admin_url_can_be_configured(self):
        """
        Test: Verificar que la URL de admin se puede configurar.
        """
        from drfmaderas.urls import ADMIN_URL

        # Verificar que ADMIN_URL está definido
        self.assertIsNotNone(ADMIN_URL)

        # Verificar que termina en '/'
        self.assertTrue(ADMIN_URL.endswith('/'))
