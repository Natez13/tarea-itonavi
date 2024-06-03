

## Demo

https://tarea-itonavi.vercel.app

# Documentación de la API de Productos

La API tiene la finalidad de gestionar productos y sus categorías. La API está construida utilizando Flask y proporciona varios endpoints para obtener productos por categoría, buscar productos, obtener productos con paginación y calcular el número total de páginas.

## Instalación

Para instalar y ejecutar este proyecto, siga estos pasos:

1. Clona el repositorio:

    ```
    git clone https://github.com/usuario/tarea-itonavi.git
    ```

2. Navega al directorio del proyecto:

    ```
    cd tarea-itonavi
    ```

3. Instala las dependencias:

    ```
    pip install -r requirements.txt
    ```

4. Configura tu base de datos en `api/database.py`.

5. Ejecuta la aplicación:

    ```
    flask run
    ```



## Buscar Productos
**GET /search**
Este endpoint busca productos por nombre.

### Parámetros:

-**q**: Término de búsqueda (obligatorio)

### Respuesta Exitosa:

```json

[
    {
        "id": 1,
        "name": "Categoria 1",
        "products": [
            {
                "id": 101,
                "name": "Producto 1",
                "url_image": "http://imagen.com/1.jpg",
                "price": 100.0,
                "discount": 10
            },
            ...
        ]
    },
    ...
]
```

### Respuesta en caso de error:

```json

{
    "error": "No se proporcionó un término de búsqueda"
}
```

```json

{
    "error": "No se pudo conectar a la base de datos"
}
```

Obtener Productos con Paginación
**GET /products**
Este endpoint devuelve una lista paginada de productos, con opciones de ordenamiento y filtrado.

### Parámetros de Paginación:

- **page**: Número de página (opcional, por defecto 1)
- **items_per_page**: Número de ítems por página (opcional, por defecto 10)
### Parámetros de Ordenamiento:

- **sort_by**: Ordenar por precio (price_asc para ascendente, price_desc para descendente)

### Parámetros de Filtro:

- **filter_by**: Filtrar por discount o price
- **min_price**: Precio mínimo (opcional, por defecto 0)
- **max_price**: Precio máximo (opcional, por defecto 10000000)

### Respuesta Exitosa:

```json
[
    {
        "id": 1,
        "name": "Categoria 1",
        "products": [
            {
                "id": 101,
                "name": "Producto 1",
                "url_image": "http://imagen.com/1.jpg",
                "price": 100.0,
                "discount": 10
            },
            ...
        ]
    },
    ...
]
```

### Respuesta en caso de error:

```json
{
    "error": "No se pudo conectar a la base de datos"
}
```

Obtener el Número Total de Páginas
**GET /total_pages**
Este endpoint calcula el número total de páginas basándose en los filtros y el número de ítems por página.

### Parámetros:

- **items_per_page**: Número de ítems por página (opcional, por defecto 10)
- **filter_by**: Filtrar por discount o price (opcional)
- **min_price**: Precio mínimo (opcional, por defecto 0)
- **max_price**: Precio máximo (opcional, por defecto 10000000)
### Respuesta Exitosa:

```json
{
    "total_pages": 10
}
```
### Respuesta en caso de error:

```json
{
    "error": "No se pudo conectar a la base de datos"
}
```

# Documentación del Front-end de Productos

## Componentes

### Lista de Productos

- **Elemento**: `div#searchResults`
  - **Descripción**: Muestra los productos recuperados de la API después de una búsqueda, ordenamiento o filtrado.
  - **Estructura**: Una serie de tarjetas de producto, cada una mostrando el nombre del producto, la categoría, una imagen, el precio y el descuento.

### Paginación

- **Elemento**: `ul#pagination`
  - **Descripción**: Proporciona botones para navegar entre las páginas de resultados.
  - **Estructura**: Botones "Anterior" y "Siguiente", con el número de página actual entre ellos.

### Funcionalidades

#### Búsqueda

- **Elemento**: `input#searchInput`
  - **Descripción**: Permite al usuario ingresar un término de búsqueda para encontrar productos.
  - **Evento**: Se activa al presionar la tecla "Enter" después de ingresar un término de búsqueda.
  - **Acción**: Realiza una solicitud GET a la API `/search?q={query}` y muestra los resultados.

#### Paginación

- **Elementos**: `button#prevPage`, `button#nextPage`
  - **Descripción**: Permite al usuario navegar entre las páginas de resultados.
  - **Evento**: Se activa al hacer clic en los botones "Anterior" o "Siguiente".
  - **Acción**: Realiza una solicitud GET a la API `/products?page={page}&items_per_page={itemsPerPage}` y muestra los resultados de la página correspondiente.

#### Ordenamiento

- **Elementos**: `button#sortAsc`, `button#sortDesc`
  - **Descripción**: Permite al usuario ordenar los productos por precio de forma ascendente o descendente.
  - **Evento**: Se activa al hacer clic en los botones "Ordenar Asc" o "Ordenar Desc".
  - **Acción**: Realiza una solicitud GET a la API `/products?page={currentPage}&items_per_page={itemsPerPage}&sort_by=price_asc` o `price_desc` según corresponda, y muestra los resultados ordenados.

#### Filtrado por Precio

- **Elemento**: `button#filterPrice`
  - **Descripción**: Permite al usuario filtrar los productos por rango de precio.
  - **Evento**: Se activa al hacer clic en el botón "Filtrar Precio".
  - **Acción**: Muestra un cuadro de diálogo para ingresar el precio mínimo y máximo, y luego realiza una solicitud GET a la API `/products?page={currentPage}&items_per_page={itemsPerPage}&filter_by=price&min_price={minPrice}&max_price={maxPrice}` y muestra los resultados filtrados.

## Interacción con la API

El front-end interactúa con la API de productos a través de solicitudes GET a varios endpoints:

- `/search?q={query}`: Para buscar productos por nombre.
- `/products?page={page}&items_per_page={itemsPerPage}&sort_by={sortOrder}`: Para obtener productos paginados y ordenados.
- `/total_pages`: Para obtener el número total de páginas de resultados.
