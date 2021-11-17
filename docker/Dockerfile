FROM ubuntu:20.04

ENV HOME=/root

RUN set -xe \
    && echo "****** Install packages with apt ******" \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y --no-install-recommends \
        python3 python3-setuptools \
        python3-pip\
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install kubernetes requests \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y python3-pip python3-setuptools \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && rm -rf /tmp/* \
    && apt-get clean \
    \
    && echo "****** Making Code Dir ******" \
    && mkdir -p /nsx-natter \
    && mkdir -p /root/.kube

COPY ./ /nsx-natter

CMD ["/nsx-natter/k8s_nsx_natter.py"]
ENTRYPOINT ["python3"]