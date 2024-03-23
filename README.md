# Rag_Studio
vector rag creation servers

#Install

#Build image
docker build -t ragstudio .

#Run Container
docker run -it -p 8501:8501 --name Rag-Studio ragstudio

#Access localhost from browser

http://localhost:8501/
