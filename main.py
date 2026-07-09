from fastapi import FastAPI, HTTPException, UploadFile, File
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

# S3 Configuration
BUCKET_NAME = "vikash-prod-user-uploads"
REGION = "ap-south-1"

# boto3 automatically uses IAM Role — no credentials needed!
s3 = boto3.client('s3', region_name=REGION)

@app.get("/")
def home():
    return {"message": "FastAPI + S3 is live! 🚀"}

@app.post("/upload-photo/")
async def upload_photo(file: UploadFile = File(...)):
    try:
        # Upload file to S3 profiles folder
        file_key = f"profiles/{file.filename}"
        
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": file.content_type}
        )
        
        # Generate presigned URL for 1 hour
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=3600
        )
        
        return {
            "message": "Photo uploaded successfully!",
            "filename": file.filename,
            "s3_key": file_key,
            "view_url": url,
            "expires_in": "1 hour"
        }
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/my-photo/{filename}")
def get_photo(filename: str):
    try:
        file_key = f"profiles/{filename}"
        
        # Generate presigned URL
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=3600
        )
        
        return {
            "filename": filename,
            "view_url": url,
            "expires_in": "1 hour"
        }
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/my-photo/{filename}")
def delete_photo(filename: str):
    try:
        file_key = f"profiles/{filename}"
        
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )
        
        return {
            "message": "Photo deleted successfully!",
            "filename": filename
        }
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/")
def get_products():
    return [
        {"id": 1, "name": "Dell XPS", "price": 80000},
        {"id": 2, "name": "MacBook Pro", "price": 150000},
        {"id": 3, "name": "HP Pavilion", "price": 55000}
    ]