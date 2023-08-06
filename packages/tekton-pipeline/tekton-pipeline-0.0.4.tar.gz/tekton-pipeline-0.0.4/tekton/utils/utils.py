import os

def is_running_in_k8s():
    return os.path.isdir('/var/run/secrets/kubernetes.io/')


def get_current_k8s_namespace():
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
        return f.readline()


def get_default_target_namespace():
    if not is_running_in_k8s():
        return 'default'
    return get_current_k8s_namespace()


def get_tekton_namespace(tekton):
    tekton_namespace = tekton.metadata.namespace
    namespace = tekton_namespace or get_default_target_namespace()
    return namespace

def get_tekton_plural(tekton):
    tekton_plural = str(tekton.kind).lower() + "s"
    return tekton_plural
