## Image Upload
` POST /api/upload `

Request (multipart/formdata):
```
image: (binary-data)
username: (string)
filter: (string)
private: (on|off)
```

Response (JSON):
```json
{
  "status": "success",
  "image_url": "/media/proc/image1.5678.png"
}
```

## List Images
` GET /api/list_images `

Response (JSON):
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 1, 
      "face_count": 1,
      "filter_used": "filter1",
      "image_url": "/media/proc/image1.5678.png",
      "username": "user1",
      "timestamp": 1619567000
    },
    {
      "id": 2, 
      "face_count": 2,
      "filter_used": "random",
      "image_url": "/media/proc/image2.1234.png",
      "username": "user2",
      "timestamp": 1619567001
    }
  ]
}
```

## Error Response
Response (JSON):
```json
{
  "status": "error",
  "message": "Error message to display to user"
}
```