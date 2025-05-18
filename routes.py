import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from src.agnets.content_extractor import Contentextractor
from src.agnets.summarizer import Summarizer
from src.agnets.slide_generator import SlideGenerator
from src.agnets.imagegenerator import ImageGenerator

router = APIRouter()

# Define directories
UPLOAD_DIR = "uploaded_files"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # ✅ Clear previous files
        for old_file in os.listdir(UPLOAD_DIR):
            os.remove(os.path.join(UPLOAD_DIR, old_file))

        # ✅ Save the new file
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        return {"filename": file.filename, "message": "File uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/generator/")
async def generate_presentation():
    """Runs the AI pipeline to generate PowerPoint slides based on uploaded files."""

    try:
        extractor = Contentextractor(directory=UPLOAD_DIR)
        extracted_content = extractor.extract_from_directory()

        if not extracted_content:
            raise HTTPException(status_code=400, detail="No content extracted from uploaded documents.")

        summarizer = Summarizer()
        image_generator = ImageGenerator()
        slide_generator = SlideGenerator(output_dir=OUTPUT_DIR)

        summaries = {}
        for filename, text in extracted_content.items():
            print(f"📄 Processing file: {filename}")
            summary = summarizer.summarize_text(text)
            summaries[filename] = summary
            print(f"✅ Summary generated for {filename}")

        images_by_file = image_generator.generate_images_for_summaries(summaries)

        for filename, summary in summaries.items():
            summary_points = summary.split("\n")
            slide_generator.create_slide_deck(
                filename,
                summary_points,
                images=images_by_file.get(filename, [])
            )

        pptx_path = os.path.join(OUTPUT_DIR, "generated_presentation.pptx")
        print(f"✅ Presentation saved to: {pptx_path}")

        if not os.path.exists(pptx_path):
            raise HTTPException(status_code=404, detail="Presentation file not found after generation.")

        return {
            "message": "Slide generated!",
            "download_url": f"/download/?filename=generated_presentation.pptx"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()  # ✅ This will show the full error
        raise HTTPException(status_code=500, detail=f"Error in generator: {str(e)}")


@router.get("/download/")
async def download_presentation(filename: str = Query(...)):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found.")
