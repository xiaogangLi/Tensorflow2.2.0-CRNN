# crnn_by_tensorflow2.2.0



## Docker中tensorflow serving启动命令

### CPU

```
docker run --name tfserving-crnn \
        --hostname tfserving-crnn \
        -tid \
        --restart=on-failure:10 \
        -p 8500:8500 \
        -p 8501:8501 \
        --mount type=bind,source=/root/python_project/jupyter_file/output,target=/models \
        -e MODEL_NAME=crnn \
        -t tensorflow/serving &
```

### GPU

```
docker run --name tfserving-crnn \
        --hostname tfserving-crnn \
        -tid \
        --restart=on-failure:10 \
        -p 8500:8500 \
        -p 8501:8501 \
        --mount type=bind,source=/root/python_project/jupyter_file/output,target=/models \
        -e MODEL_NAME=crnn \
        -t tensorflow/serving:latest-gpu &
```