#!/bin/bash

PYTHONPATH=D:/software/python
PROJSROOT=D:/projects/pytypes2/subjects100/
LIBPATHS="${PYTHONPATH}:${PYTHONPATH}/Lib/"
OUTPUTROOT=D:/projects/pytypes2/pysonar_data100/

#PROJDIRS[0]=ajenti/
PROJDIRS[1]=TheAlgorithms/
PROJDIRS[2]=youtube-dl/
#PROJDIRS[3]=models/
#PROJDIRS[4]=nvbn/
PROJDIRS[5]=django/
#PROJDIRS[6]=flask/
#PROJDIRS[7]=keras/
#PROJDIRS[8]=httpie/
#PROJDIRS[9]=ansible/
#PROJDIRS[10]=transformers/
#PROJDIRS[11]=scikit-learn/
#PROJDIRS[12]=requests/
PROJDIRS[13]=core/
#PROJDIRS[14]=scrapy/
#PROJDIRS[15]=you-get/
#PROJDIRS[16]=face_recognition/
PROJDIRS[17]=superset/
PROJDIRS[18]=cpython/
#PROJDIRS[19]=faceswap/
#PROJDIRS[20]=manim/
#PROJDIRS[21]=shadowsocks/
PROJDIRS[22]=fastapi/
#PROJDIRS[23]=XX-Net/
PROJDIRS[24]=localstack/
#PROJDIRS[25]=12306/
#PROJDIRS[26]=pandas/
PROJDIRS[27]=sentry/
#PROJDIRS[28]=bert/
#PROJDIRS[29]=certbot/
#PROJDIRS[30]=DeepFaceLab/
PROJDIRS[31]=rich/
#PROJDIRS[32]=sherlock/
#PROJDIRS[33]=Real-Time-Voice-Cloning/
#PROJDIRS[34]=Detectron/
#PROJDIRS[35]=gym/
PROJDIRS[36]=geekcomputers/
#PROJDIRS[37]=HanLP/
#PROJDIRS[38]=YouCompleteMe/
#PROJDIRS[39]=compose/
#PROJDIRS[40]=mitmproxy/
#PROJDIRS[41]=pipenv/
PROJDIRS[42]=airflow/
#PROJDIRS[43]=ItChat/
#PROJDIRS[44]=black/
#PROJDIRS[45]=django-rest-framework/
#PROJDIRS[46]=algo/
#PROJDIRS[47]=pytorch-tutorial/
PROJDIRS[48]=spaCy/
#PROJDIRS[49]=sqlmap/
#PROJDIRS[50]=Mask_RCNN/
#PROJDIRS[51]=tornado/
#PROJDIRS[52]=ML-From-Scratch/
#PROJDIRS[53]=algorithms/
#PROJDIRS[54]=python-fire/
#PROJDIRS[55]=redash/
#PROJDIRS[56]=tqdm/
#PROJDIRS[57]=glances/
#PROJDIRS[58]=hosts/
#PROJDIRS[59]=celery/
#PROJDIRS[60]=numpy/
#PROJDIRS[61]=detectron2/
#PROJDIRS[62]=magenta/
#PROJDIRS[63]=spleeter/
#PROJDIRS[64]=examples/
#PROJDIRS[65]=locust/
#PROJDIRS[66]=ray/
#PROJDIRS[67]=jumpserver/
PROJDIRS[68]=Paddle/
PROJDIRS[69]=python-telegram-bot/
#PROJDIRS[70]=poetry/
#PROJDIRS[71]=mmdetection/
#PROJDIRS[72]=bokeh/
#PROJDIRS[73]=pytorch-CycleGAN-and-pix2pix/
#PROJDIRS[74]=sanic/
#PROJDIRS[75]=pyspider/
#PROJDIRS[76]=ipython/
#PROJDIRS[77]=streamlit/
#PROJDIRS[78]=cookiecutter/
#PROJDIRS[79]=dash/
#PROJDIRS[80]=luigi/
#PROJDIRS[81]=labelImg/
#PROJDIRS[82]=PySnooper/
#PROJDIRS[83]=zipline/
#PROJDIRS[84]=wechat_jump_game/
#PROJDIRS[85]=zulip/
#PROJDIRS[86]=pytorch-lightning/
PROJDIRS[87]=matplotlib/
#PROJDIRS[88]=diagrams/
#PROJDIRS[89]=avatarify-python/
#PROJDIRS[90]=kivy/
#PROJDIRS[91]=fairseq/
#PROJDIRS[92]=jax/
#PROJDIRS[93]=fabric/
#PROJDIRS[94]=InstaPy/
#PROJDIRS[95]=prophet/
#PROJDIRS[96]=magic-wormhole/
PROJDIRS[97]=cryptography/
#PROJDIRS[98]=Ciphey/
#PROJDIRS[99]=PySyft/
#PROJDIRS[100]=RsaCtfTool/
#PROJDIRS[101]=pycrypto/
#PROJDIRS[102]=laravel-hashids/
PROJDIRS[103]=pynacl/
#PROJDIRS[104]=paramiko/
#PROJDIRS[105]=RsaCtfTool/
#PROJDIRS[106]=PaddleOCR/
#PROJDIRS[107]=autojump/

JAR=D:/projects/pytypes2/src/Detection/pystyping-3.0-milestone.jar

for PROJDIR in "${PROJDIRS[@]}"; do
	echo -e "Extracting ${PROJDIR}..."
        java -jar "${JAR}" "${PROJSROOT}${PROJDIR}" "${LIBPATHS}" "${OUTPUTROOT}${PROJDIR}" "-clearcache"
        echo -e "----------------------------\n"
done





