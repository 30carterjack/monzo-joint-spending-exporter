FROM mcr.microsoft.com/devcontainers/base:jammy
LABEL Description="monzo_budget_tracker_devcontainer"

ARG USERNAME=vscode

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gpg \
    wget \
    python3-venv

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo "$SNIPPET" >> "/home/$USERNAME/.bashrc"

RUN python3 -m venv /opt/venv/
RUN mkdir -p /tmp/pyreqs
COPY ./requirements.txt /tmp/pyreqs/requirements.txt
RUN /opt/venv/bin/pip install -r /tmp/pyreqs/requirements.txt

ENTRYPOINT [ "/bin/bash" ]