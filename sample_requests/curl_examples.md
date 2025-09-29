# Sample curl requests

## Text
curl -X POST http://localhost:8000/v1/process/text \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: demo-secret-key' \
  -d '{"input_id":"demo-1","text":"Hello, this is a demo input."}'

## Image
curl -X POST http://localhost:8000/v1/process/image \
  -H 'X-API-KEY: demo-secret-key' \
  -F 'input_id=img-1' -F 'image=@./sample.png'
