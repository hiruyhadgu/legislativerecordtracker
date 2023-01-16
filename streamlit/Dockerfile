# frontend/Dockerfile
FROM python:3.11

WORKDIR /streamlit

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /streamlit

# EXPOSE 8501

# CMD streamlit run About.py

CMD sh setup.sh && streamlit run About.py