#conda create -n hack38 python=3.8
#conda activate hack38
pip install -r requirements.txt
docker pull redis
docker run -d --name redis-server -p 6379:6379 redis