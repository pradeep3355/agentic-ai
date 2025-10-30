from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.agent_service import AgentService
import os
from app.core.s3_bucket import s3_client, S3_BUCKET
from app.core.logger import logger
import uuid
from botocore.exceptions import ClientError
from fastapi import status
from typing import Optional

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    thread_id: str


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):

    agent_service = AgentService()

    try:
        response = await agent_service.process_message(
            user_message=request.message,
            thread_id=request.thread_id,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), description: Optional[str] = None):
    """
    Upload a file to Amazon S3 bucket

    Args:
        file: The file to upload
        description: Optional description of the file

    Returns:
        Dictionary containing the S3 URL and file metadata
    """
    try:
        # Generate a unique filename to prevent overwrites
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Upload file to S3
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET,
            unique_filename,
            ExtraArgs={
                "ContentType": file.content_type,
                "Metadata": {
                    "original_filename": file.filename,
                    "description": description or "",
                },
            },
        )

        # Generate the public URL
        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{unique_filename}"

        logger.info(
            f"File uploaded to S3: {file.filename}",
            extra={
                "s3_key": unique_filename,
                "file_size": file.size,
                "content_type": file.content_type,
            },
        )

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "s3_key": unique_filename,
            "file_url": file_url,
            "content_type": file.content_type,
            "description": description,
        }

    except ClientError as e:
        logger.error(f"S3 upload error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file to S3: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}",
        )
