"""Flask web application for warehouse management."""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# In-memory storage for warehouses and ID counter
warehouses = {}
id_counter = [0]


def get_next_id():
    """Get the next available warehouse ID."""
    id_counter[0] += 1
    return id_counter[0]


@app.route('/')
def index():
    """Display the home page with list of warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['POST'])
def create_warehouse():
    """Create a new warehouse with the specified capacity."""
    try:
        capacity = float(request.form.get('capacity', 0))
        if capacity < 0:
            flash('Capacity must be 0 or positive.', 'error')
            return redirect(url_for('index'))

        warehouse_id = get_next_id()
        warehouses[warehouse_id] = {
            'varasto': Varasto(capacity),
            'name': f'Warehouse {warehouse_id}'
        }
        flash(f'Warehouse {warehouse_id} created successfully.', 'success')
    except ValueError:
        flash('Invalid capacity value.', 'error')

    return redirect(url_for('index'))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse by its ID."""
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
        flash(f'Warehouse {warehouse_id} deleted successfully.', 'success')
    else:
        flash(f'Warehouse {warehouse_id} not found.', 'error')

    return redirect(url_for('index'))


@app.route('/add/<int:warehouse_id>', methods=['POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    if warehouse_id not in warehouses:
        flash(f'Warehouse {warehouse_id} not found.', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be positive.', 'error')
            return redirect(url_for('index'))

        varasto = warehouses[warehouse_id]['varasto']
        available_space = varasto.paljonko_mahtuu()

        if amount > available_space:
            flash(
                f'Cannot add {amount}. Only {available_space} space available.',
                'error'
            )
        else:
            varasto.lisaa_varastoon(amount)
            flash(f'Added {amount} items to Warehouse {warehouse_id}.', 'success')
    except ValueError:
        flash('Invalid amount value.', 'error')

    return redirect(url_for('index'))


@app.route('/remove/<int:warehouse_id>', methods=['POST'])
def remove_items(warehouse_id):
    """Remove items from a warehouse."""
    if warehouse_id not in warehouses:
        flash(f'Warehouse {warehouse_id} not found.', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be positive.', 'error')
            return redirect(url_for('index'))

        varasto = warehouses[warehouse_id]['varasto']
        removed = varasto.ota_varastosta(amount)
        flash(
            f'Removed {removed} items from Warehouse {warehouse_id}.',
            'success'
        )
    except ValueError:
        flash('Invalid amount value.', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')
