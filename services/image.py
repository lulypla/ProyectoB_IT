import base64

import cloudinary
import cloudinary.uploader



def upload_image(image_data):
    cloudinary.config(
        cloud_name="da29ifelj",
        api_key="949499613611759",
        api_secret="v05os3Owzc3SrB8T-KSUMBBY3e4"
    )

    decoded = base64.decodebytes(image_data.encode())
    url = cloudinary.uploader.upload(decoded)
    return url['secure_url']