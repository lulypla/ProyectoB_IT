import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = "da29ifelj",
  api_key = "949499613611759",
  api_secret = "v05os3Owzc3SrB8T-KSUMBBY3e4"
)


def upload_image(image_data):
    url = cloudinary.uploader.upload(image_data)
    return url['secure_url']