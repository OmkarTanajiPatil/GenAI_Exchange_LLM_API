from fastapi import FastAPI, Body, HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from database import db
import base64

from server import app  # Assuming server.py contains the FastAPI app instance

async def update_product(product_id: str, fields: Dict[str, Any]):
    """
    Generic product updater.
    """
    try:
        result = await db["product"].update_one(
            {"_id": ObjectId(product_id)},
            {"$set": fields},
            upsert=True,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DB update failed: {str(e)}")


@app.post("/store_title/")
async def api_store_title(product_id: str = Body(...), title: str = Body(...)):
    await update_product(product_id, {"title": title})
    return {"status": "success"}


@app.post("/store_story/")
async def api_store_story(product_id: str = Body(...), story: str = Body(...)):
    await update_product(product_id, {"story": story})
    return {"status": "success"}


@app.post("/store_image/")
async def api_store_image(product_id: str = Body(...), image_base64: str = Body(...)):
    """
    Accepts base64 string of an image and stores it in MongoDB under 'image_base64'.
    """
    try:
        # Optional: validate base64
        base64.b64decode(image_base64)  # will raise error if invalid

        # Save in DB
        await update_product(product_id, {"image_base64": image_base64})
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid base64 or DB error: {str(e)}"
        )


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
