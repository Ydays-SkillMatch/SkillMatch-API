FROM python:3.12.6-slim



RUN apt-get update && apt-get install -y git zsh curl libpq-dev python3-dev build-essential gcc g++ && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    rustc --version && cargo --version

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --no-deps -r requirements.txt


EXPOSE ${PORT}

CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:${PORT}"]