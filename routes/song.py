from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary, cloudinary.uploader
import uuid

router = APIRouter()

# Configuration
cloudinary.config(
    cloud_name="dacv5nfo3",
    api_key="492154986287546",
    api_secret="18eYoPELByLX9Bfz3Hs-i8HBqnw",  # Click 'View API Keys' above to copy your API secret
    secure=True,
)


@router.post("/upload")
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
    auth_dict=Depends(auth_middleware),
):
    song_id = str(uuid.uuid4())
    song_res = cloudinary.uploader.upload(
        song.file, folder=f"songs/{song_id}", resource_type="auto"
    )
    print(song_res)
    thumbnail_res = cloudinary.uploader.upload(
        thumbnail.file, folder=f"songs/{song_id}", resource_type="image"
    )
    print(thumbnail_res)
    return "ok"
