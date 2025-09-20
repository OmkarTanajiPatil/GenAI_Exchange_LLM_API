from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import os
import base64

from prompts import *

# Initialize FastAPI app
app = FastAPI(title="Artisan Product Content Generator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
# Set your API key as environment variable: export GEMINI_API_KEY="your_api_key_here"
# GEMINI_API_KEY =
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")
image_generation_model = genai.GenerativeModel("gemini-2.5-flash-image-preview")


# Response models
class TitleResponse(BaseModel):
    titles: List[str]


class StoryResponse(BaseModel):
    stories: List[str]


class GeneratedContent(BaseModel):
    success: bool
    data: dict
    message: str


def process_image(image_file: UploadFile) -> Image.Image:
    """Process uploaded image file and return PIL Image object"""
    try:
        # Read image data
        image_data = image_file.file.read()

        # Convert to PIL Image
        image = Image.open(BytesIO(image_data))

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Artisan Product Content Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_titles": "/generate-titles",
            "generate_stories": "/generate-stories",
        },
    }


@app.post("/gen-titles", response_model=GeneratedContent)
async def generate_titles(
    user_title: str = Form(..., description="User provided title"),
    location: str = Form(..., description="Location/origin of the product"),
    category: str = Form(..., description="Product category"),
):
    """
    Generate 3 creative titles for an artisan product based on the uploaded image and context.
    """
    try:
        prompt = generate_titles_prompt(user_title, location, category)
        response = model.generate_content([prompt])
        titles_text = response.text.strip()
        titles = [title.strip() for title in titles_text.split("\n") if title.strip()]
        titles = titles[:3]
        return GeneratedContent(
            success=True,
            data={"titles": titles},
            message="Titles generated successfully",
        )
    except Exception as e:
        return GeneratedContent(
            success=False, data={}, message=f"Error generating titles: {str(e)}"
        )


@app.post("/gen-stories", response_model=GeneratedContent)
async def generate_stories(
    user_title: str = Form(..., description="User provided title"),
    location: str = Form(..., description="Location/origin of the product"),
    category: str = Form(..., description="Product category"),
    description: str = Form(..., description="User provided description"),
):
    """
    Generate 3 compelling stories for an artisan product based on the uploaded image and context.
    """
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Process the image
        processed_image = process_image(image)

        # Generate the prompt
        prompt = generate_stories_prompt(user_title, location, category, description)

        # Call Gemini API
        response = model.generate_content([prompt, processed_image])

        # Parse the response
        stories_text = response.text.strip()

        # Split stories by the marker
        stories = []
        if "---STORY---" in stories_text:
            story_parts = stories_text.split("---STORY---")
            stories = [story.strip() for story in story_parts if story.strip()]
        else:
            # Fallback: split by double newlines or assume single story
            story_parts = stories_text.split("\n\n\n")
            if len(story_parts) >= 3:
                stories = story_parts[:3]
            else:
                # If we can't parse properly, create fallback stories
                stories = [stories_text]

        # Ensure we have exactly 3 stories
        while len(stories) < 3:
            stories.append(
                f"This beautiful {category} from {location} represents the rich tradition of local craftsmanship. Each piece tells a story of dedication, skill, and cultural heritage passed down through generations."
            )
        stories = stories[:3]  # Take only first 3

        return GeneratedContent(
            success=True,
            data={"stories": stories},
            message="Stories generated successfully",
        )

    except Exception as e:
        return GeneratedContent(
            success=False, data={}, message=f"Error generating stories: {str(e)}"
        )


@app.post("/gen-images-name-category", response_model=GeneratedContent)
async def generate_images_name_category(
    image: UploadFile = File(..., description="Artisan product image"),
):
    """
    Generate 3 enhanced images for an artisan product based on the uploaded image.
    """
    try:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        processed_image = process_image(image)
        image_generation_prompt = generate_images_prompt()
        category_generation_prompt = category_prompt()
        title_generation_prompt = product_name_prompt()

        image_response = image_generation_model.generate_content(
            [processed_image, image_generation_prompt]
        )
        category_response = image_generation_model.generate_content(
            [processed_image, category_generation_prompt]
        )
        title_response = image_generation_model.generate_content(
            [processed_image, title_generation_prompt]
        )

        generated_images_data = []
        for part in image_response.candidates[0].content.parts:
            if part.inline_data:
                # The Gemini API provides image data as inline data
                img_data = part.inline_data.data
                img_str = base64.b64encode(img_data).decode("utf-8")
                generated_images_data.append(
                    f"data:{part.inline_data.mime_type};base64,{img_str}"
                )

        generated_titles = title_response.text.split("\n")
        generated_category = category_response.text.strip()

        if len(generated_images_data) == 0:
            raise Exception("API did not return any image data.")

        return GeneratedContent(
            success=True,
            data={
                "images": generated_images_data,
                "titles": generated_titles,
                "category": generated_category,
            },
            message="Images generated successfully.",
        )

    except Exception as e:
        return GeneratedContent(
            success=False, data={}, message=f"Error generating images: {str(e)}"
        )


@app.post("/gen-tags-captions", response_model=GeneratedContent)
async def generate_tags_captions(
    image: UploadFile = File(..., description="Artisan product image"),
    title: str = Form(..., description="Product title"),
    description: str = Form(..., description="Product description"),
    category: str = Form(..., description="Product category"),
    location: str = Form(..., description="Product location"),
):
    """
    Generate SEO tags, hashtags, and creative captions for an artisan product.
    """
    try:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        processed_image = process_image(image)
        prompt = generate_tags_captions_prompt(title, description, category, location)

        response = model.generate_content([prompt, processed_image])
        result_text = response.text.strip()

        # Parse the response
        seo_tags = []
        hashtags = []
        captions = []

        # Simple parsing logic (adjust based on LLM output format)
        lines = [line.strip() for line in result_text.split("\n") if line.strip()]
        for line in lines:
            if line.lower().startswith("seo tags:"):
                seo_tags = [
                    tag.strip()
                    for tag in line[len("seo tags:") :].split(",")
                    if tag.strip()
                ]
            elif line.lower().startswith("hashtags:"):
                hashtags = [
                    tag.strip()
                    for tag in line[len("hashtags:") :].split(",")
                    if tag.strip()
                ]
            elif line.lower().startswith("captions:"):
                captions = [
                    cap.strip()
                    for cap in line[len("captions:") :].split("|")
                    if cap.strip()
                ]

        # Fallback if not parsed
        if not seo_tags:
            seo_tags = [line for line in lines if line.startswith("#SEO")][:5]
        if not hashtags:
            hashtags = [line.split(" ") for line in lines if line.startswith("#")][:7]
        if not captions:
            captions = [
                line
                for line in lines
                if not line.startswith("#")
                and not line.lower().startswith("seo tags")
                and not line.lower().startswith("hashtags")
            ][:3]

        # Limit counts
        seo_tags = seo_tags[:5]
        hashtags = hashtags[:7]
        captions = captions[:3]

        return GeneratedContent(
            success=True,
            data={
                "seo_tags": seo_tags,
                "hashtags": hashtags,
                "captions": captions,
            },
            message="Tags, hashtags, and captions generated successfully.",
        )
    except Exception as e:
        return GeneratedContent(
            success=False, data={}, message=f"Error generating tags/captions: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "artisan-content-generator"}
