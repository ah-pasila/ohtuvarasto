"""Tests for the Flask web application."""

import unittest
from app import app, warehouses, id_counter


class TestWarehouseAppBase(unittest.TestCase):
    """Base class for warehouse test cases."""

    def setUp(self):
        """Set up test client and clear warehouses before each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        warehouses.clear()
        id_counter[0] = 0


class TestWarehouseIndex(TestWarehouseAppBase):
    """Test cases for the index page."""

    def test_index_page_loads(self):
        """Test that the index page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_index_shows_no_warehouses_initially(self):
        """Test that index shows no warehouses message when empty."""
        response = self.client.get('/')
        self.assertIn(b'No warehouses yet', response.data)

    def test_warehouse_displayed_on_index(self):
        """Test that created warehouse is displayed on index page."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.get('/')
        self.assertIn(b'Warehouse 1', response.data)
        self.assertIn(b'Capacity: 100', response.data)


class TestWarehouseCreate(TestWarehouseAppBase):
    """Test cases for warehouse creation."""

    def test_create_warehouse_with_valid_capacity(self):
        """Test creating a warehouse with valid positive capacity."""
        response = self.client.post('/create', data={'capacity': '100'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(warehouses), 1)
        self.assertEqual(warehouses[1]['varasto'].tilavuus, 100)

    def test_create_warehouse_with_zero_capacity(self):
        """Test creating a warehouse with zero capacity is valid."""
        response = self.client.post('/create', data={'capacity': '0'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(warehouses), 1)
        self.assertEqual(warehouses[1]['varasto'].tilavuus, 0)

    def test_create_warehouse_with_negative_capacity_fails(self):
        """Test that creating a warehouse with negative capacity fails."""
        response = self.client.post(
            '/create', data={'capacity': '-10'}, follow_redirects=True
        )
        self.assertEqual(len(warehouses), 0)
        self.assertIn(b'Capacity must be 0 or positive', response.data)

    def test_create_warehouse_with_invalid_capacity(self):
        """Test that invalid capacity value shows error."""
        response = self.client.post(
            '/create', data={'capacity': 'invalid'}, follow_redirects=True
        )
        self.assertEqual(len(warehouses), 0)
        self.assertIn(b'Invalid capacity value', response.data)

    def test_create_multiple_warehouses(self):
        """Test creating multiple warehouses."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/create', data={'capacity': '200'})
        self.client.post('/create', data={'capacity': '50'})

        self.assertEqual(len(warehouses), 3)
        self.assertEqual(warehouses[1]['varasto'].tilavuus, 100)
        self.assertEqual(warehouses[2]['varasto'].tilavuus, 200)
        self.assertEqual(warehouses[3]['varasto'].tilavuus, 50)


class TestWarehouseDelete(TestWarehouseAppBase):
    """Test cases for warehouse deletion."""

    def test_delete_warehouse(self):
        """Test deleting an existing warehouse."""
        self.client.post('/create', data={'capacity': '100'})
        self.assertEqual(len(warehouses), 1)

        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(warehouses), 0)

    def test_delete_nonexistent_warehouse(self):
        """Test deleting a non-existent warehouse shows error."""
        response = self.client.post('/delete/999', follow_redirects=True)
        self.assertIn(b'not found', response.data)


class TestWarehouseAddItems(TestWarehouseAppBase):
    """Test cases for adding items to warehouses."""

    def test_add_items_to_warehouse(self):
        """Test adding items to a warehouse."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post('/add/1', data={'amount': '50'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(warehouses[1]['varasto'].saldo, 50)

    def test_add_items_exceeding_capacity_fails(self):
        """Test that adding more items than capacity shows error."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post(
            '/add/1', data={'amount': '150'}, follow_redirects=True
        )
        self.assertIn(b'Cannot add', response.data)
        self.assertEqual(warehouses[1]['varasto'].saldo, 0)

    def test_add_items_to_nonexistent_warehouse(self):
        """Test adding items to non-existent warehouse shows error."""
        response = self.client.post(
            '/add/999', data={'amount': '50'}, follow_redirects=True
        )
        self.assertIn(b'not found', response.data)

    def test_add_negative_items_fails(self):
        """Test that adding negative amount shows error."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post(
            '/add/1', data={'amount': '-10'}, follow_redirects=True
        )
        self.assertIn(b'Amount must be positive', response.data)

    def test_add_zero_items_fails(self):
        """Test that adding zero amount shows error."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post(
            '/add/1', data={'amount': '0'}, follow_redirects=True
        )
        self.assertIn(b'Amount must be positive', response.data)

    def test_add_invalid_amount(self):
        """Test that invalid amount shows error."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post(
            '/add/1', data={'amount': 'invalid'}, follow_redirects=True
        )
        self.assertIn(b'Invalid amount value', response.data)

    def test_capacity_not_exceeded_after_multiple_additions(self):
        """Test that capacity is not exceeded after multiple additions."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/add/1', data={'amount': '40'})
        self.client.post('/add/1', data={'amount': '40'})

        response = self.client.post(
            '/add/1', data={'amount': '30'}, follow_redirects=True
        )
        self.assertIn(b'Cannot add', response.data)
        self.assertEqual(warehouses[1]['varasto'].saldo, 80)


class TestWarehouseRemoveItems(TestWarehouseAppBase):
    """Test cases for removing items from warehouses."""

    def test_remove_items_from_warehouse(self):
        """Test removing items from a warehouse."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/add/1', data={'amount': '50'})

        response = self.client.post('/remove/1', data={'amount': '20'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(warehouses[1]['varasto'].saldo, 30)

    def test_remove_more_than_available(self):
        """Test removing more items than available."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/add/1', data={'amount': '50'})

        self.client.post(
            '/remove/1', data={'amount': '100'}, follow_redirects=True
        )
        self.assertEqual(warehouses[1]['varasto'].saldo, 0)

    def test_remove_items_from_nonexistent_warehouse(self):
        """Test removing items from non-existent warehouse shows error."""
        response = self.client.post(
            '/remove/999', data={'amount': '50'}, follow_redirects=True
        )
        self.assertIn(b'not found', response.data)

    def test_remove_negative_items_fails(self):
        """Test that removing negative amount shows error."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/add/1', data={'amount': '50'})

        response = self.client.post(
            '/remove/1', data={'amount': '-10'}, follow_redirects=True
        )
        self.assertIn(b'Amount must be positive', response.data)

    def test_remove_zero_items_fails(self):
        """Test that removing zero amount shows error."""
        self.client.post('/create', data={'capacity': '100'})
        self.client.post('/add/1', data={'amount': '50'})

        response = self.client.post(
            '/remove/1', data={'amount': '0'}, follow_redirects=True
        )
        self.assertIn(b'Amount must be positive', response.data)

    def test_remove_invalid_amount(self):
        """Test that invalid removal amount shows error."""
        self.client.post('/create', data={'capacity': '100'})

        response = self.client.post(
            '/remove/1', data={'amount': 'invalid'}, follow_redirects=True
        )
        self.assertIn(b'Invalid amount value', response.data)


if __name__ == '__main__':
    unittest.main()
