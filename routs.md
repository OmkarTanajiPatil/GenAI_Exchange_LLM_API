
# API Routes

This file lists all the API routes defined in the project.

## `server.py`

### GET `/`

- **Description:** Root endpoint with API information.
- **Input:** None

### POST `/gen-images-name-category`

- **Description:** Generate 3 enhanced images for an artisan product based on the uploaded image.
- **Input Type:** Form Data
- **Parameters:**
  - `image`: `UploadFile` (Artisan product image)

### POST `/gen-titles`

- **Description:** Generate 3 creative titles for an artisan product.
- **Input Type:** Form Data
- **Parameters:**
  - `user_title`: `str` (User provided title)
  - `location`: `str` (Location/origin of the product)
  - `category`: `str` (Product category)

### POST `/gen-stories`

- **Description:** Generate 3 compelling stories for an artisan product.
- **Input Type:** Form Data
- **Parameters:**
  - `user_title`: `str` (User provided title)
  - `location`: `str` (Location/origin of the product)
  - `category`: `str` (Product category)
  - `description`: `str` (User provided description)

### POST `/gen-tags-captions`

- **Description:** Generate SEO tags, hashtags, and creative captions for an artisan product.
- **Input Type:** Form Data
- **Parameters:**
  - `image`: `UploadFile` (Artisan product image)
  - `title`: `str` (Product title)
  - `description`: `str` (Product description)
  - `category`: `str` (Product category)
  - `location`: `str` (Product location)

### GET `/products/`

- **Description:** Fetch all products from the database.
- **Input:** None

### GET `/health`

- **Description:** Health check endpoint.
- **Input:** None

## `store_into_db_urls.py`

### POST `/create_product`

- **Description:** Create a new product.
- **Input:** None

### POST `/store_title/`

- **Description:** Store title for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `title`: `str`

### POST `/store_story/`

- **Description:** Store story for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `story`: `str`

### POST `/store_image/`

- **Description:** Store image (base64) for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `image_base64`: `str`

### POST `/store_name_category_location/`

- **Description:** Store name, category, and location for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `name`: `str`
  - `category`: `str`
  - `location`: `str`

### POST `/store_description/`

- **Description:** Store description for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `description`: `str`

### POST `/store_caption_hashtags_seo/`

- **Description:** Store caption, hashtags, and SEO tags for a product.
- **Input Type:** JSON Body
- **Parameters:**
  - `product_id`: `str`
  - `caption`: `str`
  - `hashtags`: `List[str]`
  - `seo_tags`: `List[str]`
