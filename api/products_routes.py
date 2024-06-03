from flask import Blueprint, jsonify, request
from api.database import get_db_connection
from flask_cors import cross_origin
import math

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products_by_category', methods=['GET'])
def get_products_by_category():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                c.id as category_id, 
                c.name as category_name, 
                p.id as product_id, 
                p.name as product_name, 
                p.url_image, 
                p.price, 
                p.discount 
            FROM 
                product p 
            JOIN 
                category c 
            ON 
                p.category = c.id
            """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Agrupar productos por categoría
        categories = {}
        for row in results:
            category_id = row['category_id']
            if category_id not in categories:
                categories[category_id] = {
                    'id': category_id,
                    'name': row['category_name'],
                    'products': []
                }
            product = {
                'id': row['product_id'],
                'name': row['product_name'],
                'url_image': row['url_image'],
                'price': row['price'],
                'discount': row['discount']
            }
            categories[category_id]['products'].append(product)
        
        return jsonify(list(categories.values()))
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@product_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No se proporcionó un término de búsqueda"}), 400

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        search_query = """
            SELECT 
                p.id as product_id, 
                p.name as product_name, 
                p.url_image, 
                p.price, 
                p.discount, 
                c.id as category_id, 
                c.name as category_name
            FROM 
                product p
            JOIN 
                category c 
            ON 
                p.category = c.id
            WHERE 
                p.name LIKE %s
            """
        cursor.execute(search_query, ('%' + query + '%',))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Agrupar productos por categoría
        categories = {}
        for row in results:
            category_id = row['category_id']
            if category_id not in categories:
                categories[category_id] = {
                    'id': category_id,
                    'name': row['category_name'],
                    'products': []
                }
            product = {
                'id': row['product_id'],
                'name': row['product_name'],
                'url_image': row['url_image'],
                'price': row['price'],
                'discount': row['discount']
            }
            categories[category_id]['products'].append(product)
        
        return jsonify(list(categories.values()))
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500


@product_bp.route('/products', methods=['GET'])
def get_products():
    # Parámetros de paginación
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    # Parámetros de ordenamiento
    sort_by = request.args.get('sort_by')
    if sort_by not in ['price_asc', 'price_desc']:
        sort_by = None

    # Parámetros de filtro
    filter_by = request.args.get('filter_by')
    if filter_by not in ['discount', 'price']:
        filter_by = None

    # Rango de precios para el filtro
    min_price = request.args.get('min_price', default=0, type=float)
    max_price = request.args.get('max_price', default=10000000, type=float)

    # Conexión a la base de datos
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        offset = (page - 1) * items_per_page

        # Construir la consulta base
        query = """
            SELECT 
                p.id as product_id, 
                p.name as product_name, 
                p.url_image, 
                p.price, 
                p.discount, 
                c.id as category_id, 
                c.name as category_name
            FROM 
                product p
            JOIN 
                category c 
            ON 
                p.category = c.id
        """

        # Aplicar filtro
        if filter_by:
            query += f" WHERE p.{filter_by} BETWEEN %s AND %s"

        # Aplicar ordenamiento
        if sort_by:
            order = 'ASC' if sort_by == 'price_asc' else 'DESC'
            query += f" ORDER BY p.price {order}"

        # Aplicar paginación
        query += f" LIMIT %s OFFSET %s"

        # Ejecutar la consulta
        if filter_by:
            cursor.execute(query, (min_price, max_price, items_per_page, offset))
        else:
            cursor.execute(query, (items_per_page, offset))
        
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Agrupar productos por categoría
        categories = {}
        for row in results:
            category_id = row['category_id']
            if category_id not in categories:
                categories[category_id] = {
                    'id': category_id,
                    'name': row['category_name'],
                    'products': []
                }
            product = {
                'id': row['product_id'],
                'name': row['product_name'],
                'url_image': row['url_image'],
                'price': row['price'],
                'discount': row['discount']
            }
            categories[category_id]['products'].append(product)

        return jsonify(list(categories.values()))
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500


@product_bp.route('/total_pages', methods=['GET'])
def get_total_pages():
    items_per_page = request.args.get('items_per_page', default=10, type=int)
    filter_by = request.args.get('filter_by')
    min_price = request.args.get('min_price', default=0, type=float)
    max_price = request.args.get('max_price', default=10000000, type=float)

    # Conexión a la base de datos
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)

        # Construir la consulta base
        query = """
            SELECT 
                COUNT(*) as total_count
            FROM 
                product p
        """

        # Aplicar filtro
        if filter_by:
            query += f" WHERE p.{filter_by} BETWEEN %s AND %s"

        # Ejecutar la consulta
        if filter_by:
            cursor.execute(query, (min_price, max_price))
        else:
            cursor.execute(query)
        
        result = cursor.fetchone()
        total_count = result['total_count']
        total_pages = math.ceil(total_count / items_per_page)

        cursor.close()
        connection.close()

        return jsonify({"total_pages": total_pages})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

