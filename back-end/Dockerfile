FROM python
COPY backend.py /root/backend.py
COPY config.py /root/config.py
COPY database_manager.py /root/database_manager.py
COPY requirements.txt /root/requirements.txt

RUN pip3 install --no-cache-dir pymysql
RUN pip3 install --no-cache-dir -r /root/requirements.txt

ENTRYPOINT ["python3"]

CMD ["/root/backend.py"]