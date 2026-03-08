# Python image use karein
FROM python:3.9

# Working directory set karein
WORKDIR /code

# Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pura code copy karein
COPY . .

# Folders create karein (Just in case)
RUN mkdir -p Pending_Approval Approved Rejected Logs

# Port 7860 expose karein (HF ka default)
EXPOSE 7860

# App aur Watcher dono ko ek saath chalane ke liye command
CMD python main.py & uvicorn app:app --host 0.0.0.0 --port 7860