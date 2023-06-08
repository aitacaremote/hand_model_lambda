# lambda base image for Docker from AWS
FROM public.ecr.aws/lambda/python:3.10
# install packages
RUN yum install -y gcc-c++ pkgconfig poppler-cpp-devel
RUN yum install libglvnd-glx -y
# copy all code and lambda handler
COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt

COPY src ./src
RUN python3 -m pip install -r src/requirements.txt
RUN python3 -m pip install -e src/.
COPY lambda_handler.py ./
COPY fit_models ./fit_models
COPY CoinTranslate.py ./
COPY config.py ./
COPY components ./components

ENV ENV_MODE=FALSE
ENV LOCAL_MODE=FALSE
ENV MODEL_FITTED=./fit_models/fitted.sav
ENV MODEL_LOOSE=./fit_models/loose.sav


# run lambda handler
CMD ["lambda_handler.handler"]