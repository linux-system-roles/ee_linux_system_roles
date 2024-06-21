ARG EE_BASE_IMAGE="quay.io/ansible/ansible-runner:stable-2.12-latest"
ARG EE_BUILDER_IMAGE="quay.io/ansible/ansible-builder:latest"
ARG PYCMD="/usr/bin/python3"
ARG PKGMGR_PRESERVE_CACHE=""
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS=""
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS=""

# Base build stage
FROM $EE_BASE_IMAGE as base
USER root
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ARG EE_BASE_IMAGE
ARG EE_BUILDER_IMAGE
ARG PYCMD
ARG PKGMGR_PRESERVE_CACHE
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS

COPY _build/scripts/ /output/scripts/
COPY _build/scripts/entrypoint /opt/builder/bin/entrypoint

# Galaxy build stage
FROM base as galaxy
ARG EE_BASE_IMAGE
ARG EE_BUILDER_IMAGE
ARG PYCMD
ARG PKGMGR_PRESERVE_CACHE
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS

RUN /output/scripts/check_galaxy
COPY _build /build
WORKDIR /build

RUN mkdir -p /usr/share/ansible
RUN ansible-galaxy role install $ANSIBLE_GALAXY_CLI_ROLE_OPTS -r requirements.yml --roles-path "/usr/share/ansible/roles"
RUN ANSIBLE_GALAXY_DISABLE_GPG_VERIFY=1 ansible-galaxy collection install $ANSIBLE_GALAXY_CLI_COLLECTION_OPTS -r requirements.yml --collections-path "/usr/share/ansible/collections"

# Builder build stage
FROM $EE_BUILDER_IMAGE as builder
ENV PIP_BREAK_SYSTEM_PACKAGES=1
WORKDIR /build
ARG EE_BASE_IMAGE
ARG EE_BUILDER_IMAGE
ARG PYCMD
ARG PKGMGR_PRESERVE_CACHE
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS

COPY _build/scripts/pip_install /output/scripts/pip_install
RUN /output/scripts/pip_install $PYCMD

COPY --from=galaxy /usr/share/ansible /usr/share/ansible

COPY _build/bindep.txt bindep.txt
RUN $PYCMD /output/scripts/introspect.py introspect --user-bindep=bindep.txt --write-bindep=/tmp/src/bindep.txt --write-pip=/tmp/src/requirements.txt
RUN /output/scripts/assemble

# Final build stage
FROM base as final
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ARG EE_BASE_IMAGE
ARG EE_BUILDER_IMAGE
ARG PYCMD
ARG PKGMGR_PRESERVE_CACHE
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS


COPY --from=galaxy /usr/share/ansible /usr/share/ansible

COPY --from=builder /output/ /output/
RUN /output/scripts/install-from-bindep && rm -rf /output/wheels
RUN rm -rf /output
LABEL ansible-execution-environment=true
