from fastapi import FastAPI, Body, HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from database import db
import base64, binascii
from datetime import datetime

from server import app  # assumes your FastAPI app is defined in server.py


# Generic product updater
async def update_product(product_id: str, fields: Dict[str, Any]):
    try:
        result = await db["product"].update_one(
            {"_id": ObjectId(product_id)},
            {"$set": fields},
            upsert=False,
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DB update failed: {str(e)}")


# Create a new product
@app.post("/create_product")
async def create_product():
    new_product = {
        "name": "",
        "category": "",
        "location": "",
        "description": "",
        "title": "",
        "story": "",
        "caption": "",
        "hashtags": [],
        "seo_tags": [],
        "image_base64": "",
        "timestamp": datetime.utcnow(),  # added timestamp
    }
    try:
        result = await db["product"].insert_one(new_product)
        return {"status": "success", "product_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not create product: {str(e)}"
        )


# Store title
@app.post("/store_title/")
async def api_store_title(product_id: str = Body(...), title: str = Body(...)):
    await update_product(product_id, {"title": title})
    return {"status": "success"}


# Store story
@app.post("/store_story/")
async def api_store_story(product_id: str = Body(...), story: str = Body(...)):
    await update_product(product_id, {"story": story})
    return {"status": "success"}


# Store image (base64)
@app.post("/store_image/")
async def api_store_image(product_id: str = Body(...), image_base64: str = Body(...)):
    try:
        base64.b64decode(image_base64)
        await update_product(product_id, {"image_base64": image_base64})
        return {"status": "success"}
    except binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 string")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DB error: {str(e)}")


# Store name, category, location
@app.post("/store_name_category_location/")
async def store_name_category_location(
    product_id: str = Body(...),
    name: str = Body(...),
    category: str = Body(...),
    location: str = Body(...),
):
    await update_product(
        product_id, {"name": name, "category": category, "location": location}
    )
    return {"status": "success"}


# Store description
@app.post("/store_description/")
async def store_description(
    product_id: str = Body(...),
    description: str = Body(...),
):
    await update_product(product_id, {"description": description})
    return {"status": "success"}


# Store caption, hashtags, SEO tags
@app.post("/store_caption_hashtags_seo/")
async def api_store_caption_hashtags_seo(
    product_id: str = Body(...),
    caption: str = Body(...),
    hashtags: List[str] = Body(...),
    seo_tags: List[str] = Body(...),
):
    await update_product(
        product_id, {"caption": caption, "hashtags": hashtags, "seo_tags": seo_tags}
    )
    return {"status": "success"}
