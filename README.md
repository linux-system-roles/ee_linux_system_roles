# ee_linux_system_roles
[![Container Repository on Quay](https://quay.io/repository/linux-system-roles/ee_linux_system_roles/status "Container Repository on Quay")](https://quay.io/repository/linux-system-roles/ee_linux_system_roles)

Ansible supports a new feature for bundling collections and their runtime
environments, including the Ansible executable and dependencies, together in an
executable container.  This is called an Ansible Execution Environment.  This is
a [good introduction](https://www.ansible.com/blog/introduction-to-ansible-builder).

Linux System Roles is publishing an execution environment which contains the
`fedora.linux_system_roles` collection along with its dependencies.

`ee_linux_system_roles` uses the latest collection published in Galaxy, so if
you want to build an updated EE, you may have to first publish the latest
content in the `fedora.linux_system_roles` collection.  The EE version tag is
the version of the collection used to build - this is `$COLLECTION_VERSION`
below.  Check the latest version:
https://galaxy.ansible.com/fedora/linux_system_roles.  To build:
```
ansible-builder build -v 3 --container-runtime=podman \
  --file=builder.yml --tag=ee_linux_system_roles:$COLLECTION_VERSION
podman images | grep ee_linux_system_roles
```
To publish to quay, you must have an auth token for your
`${XDG_RUNTIME_DIR}/containers/auth.json`.  To obtain this token, login to your quay.io account,
go to `Account Settings`, go to `CLI Password: ` and click on `Generate
Encrypted Password`. Then use this with `podman login quay.io`.
```
podman tag ee_linux_system_roles:$COLLECTION_VERSION quay.io/linux-system-roles/ee_linux_system_roles:$COLLECTION_VERSION 
podman push quay.io/linux-system-roles/ee_linux_system_roles:$COLLECTION_VERSION
```
To publish a testing image, use the `-testing` suffix:
```
podman tag ee_linux_system_roles:$COLLECTION_VERSION quay.io/linux-system-roles/ee_linux_system_roles:$COLLECTION_VERSION-testing
podman push quay.io/linux-system-roles/ee_linux_system_roles:$COLLECTION_VERSION-testing
```
Once you use `ansible-builder`, be sure to push the files in the `context/`
directory as well.  These are the files that can be used by `podman build`
or by the `quay.io` builder. If you just want to update the
context files, you can use `ansible-builder create` instead of `ansible-builder
build`, then submit a PR for the updated files.
