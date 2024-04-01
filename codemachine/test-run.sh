docker build -t codemachine:latest .
docker run --name codemachine --network codemachine codemachine:latest