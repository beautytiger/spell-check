import re
from utils.helper import get_file_extension, walk_dir


def find_dup_line(file):
    with open(file) as f:
        lines = f.readlines()
    print_file_name = False
    pre_line = ""
    count = 1
    for l in lines:
        # clean_line = l.strip()
        clean_line = l
        if len(clean_line) > 1 and clean_line == pre_line:
            if not re.findall(r"\w+", clean_line):
                pass
            else:
                if print_file_name is False:
                    print(file)
                    print_file_name = True
                print("{:<10d}{}".format(count, l), end="")
        pre_line = clean_line
        count += 1


def project_docs(project):
    for file in walk_dir(project):
        if "vendor/" in file or "generated/" in file or "node_modules/" in file:
            continue
        if file.endswith("_test.go") or file.endswith(".pb.go"):
            continue
        if get_file_extension(file) == "md":
            find_dup_line(file)


projects = [
    #    "/home/matrix/go/src/github.com/envoyproxy/go-control-plane",
    #    "/home/matrix/go/src/github.com/prometheus/prometheus",
    #    "/home/matrix/go/src/github.com/prometheus/node_exporter",
    #    "/home/matrix/go/src/github.com/prometheus/alertmanager",
    #    "/home/matrix/go/src/github.com/prometheus/prombench",
    #    "/home/matrix/go/src/github.com/prometheus/client_golang",
    #    "/home/matrix/go/src/github.com/prometheus/procfs",
    #    "/home/matrix/go/src/go.etcd.io/etcd/",
    #    "/home/matrix/go/src/github.com/operator-framework/operator-sdk",
    #    "/home/matrix/go/src/github.com/operator-framework/operator-lifecycle-manage",
    #    "/home/matrix/go/src/github.com/operator-framework/operator-metering",
    #    "/home/matrix/go/src/github.com/operator-framework/operator-registry",
    #    "/home/matrix/go/src/github.com/coredns/coredns",
    #    "/home/matrix/go/src/github.com/knative/serving",
    #    "/home/matrix/go/src/github.com/knative/eventing",
    #    "/home/matrix/go/src/github.com/projectcalico/calicoctl",
    #    "/home/matrix/go/src/github.com/projectcalico/felix",
    #    "/home/matrix/go/src/github.com/projectcalico/cni-plugin",
    #    "/home/matrix/go/src/github.com/projectcalico/libcalico-go",
    #    "/home/matrix/go/src/github.com/projectcalico/node",
    #    "/home/matrix/go/src/github.com/projectcalico/typha",
    #    "/home/matrix/go/src/istio.io/istio",
    #    "/home/matrix/go/src/istio.io/operator",
    #    "/home/matrix/go/src/istio.io/tools",
    #    "/home/matrix/go/src/istio.io/pkg",
    #    "/home/matrix/go/src/istio.io/cni",
    #    "/home/matrix/go/src/istio.io/test-infra",
    #    "/home/matrix/go/src/github.com/dragonflyoss/Dragonfly",
    #    "/home/matrix/go/src/k8s.io/kops",
    #    "/home/matrix/go/src/github.com/kubeedge/kubeedge",
    #    "/home/matrix/go/src/vitess.io/vitess",
    #    "/home/matrix/go/src/k8s.io/minikube",
    #    "/home/matrix/go/src/k8s.io/kubeadm",
    #    "/home/matrix/go/src/github.com/containerd/containerd",
    #    "/home/matrix/go/src/github.com/cortexproject/cortex",
    #    "/home/matrix/go/src/kubevirt.io/kubevirt",
    #    "/home/matrix/go/src/github.com/fluxcd/flux",
    #    "/home/matrix/go/src/github.com/goharbor/harbor/src",
    #    "/home/matrix/go/src/k8s.io/ingress-nginx",
    #    "/home/matrix/go/src/github.com/jaegertracing/jaeger",
    #    "/home/matrix/go/src/sigs.k8s.io/kind",
    #    "/home/matrix/go/src/github.com/linkerd/linkerd2",
    #    "/home/matrix/go/src/github.com/nats-io/nats-server",
    #    "/home/matrix/go/src/github.com/networkservicemesh/networkservicemesh",
    #    "/home/matrix/go/src/github.com/open-telemetry/opentelemetry-service",
    #    "/home/matrix/go/src/github.com/spiffe/spire",
    #    "/home/matrix/go/src/github.com/thanos-io/thanos",
    #    "/home/matrix/go/src/github.com/virtual-kubelet/virtual-kubelet",
    #    "/home/matrix/go/src/github.com/containernetworking/plugins",
    #    "/home/matrix/go/src/github.com/containernetworking/cni",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/poseidon",
    #    "/home/matrix/go/src/sigs.k8s.io/kustomize",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/alibaba-cloud-csi-driver",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/kube-batch",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/aws-alb-ingress-controller",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-aws",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-azure",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-digitalocean",
    #    "/home/matrix/go/src/sigs.k8s.io/controller-runtime",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/cri-tools",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-ibmcloud",
    #    "/home/matrix/go/src/sigs.k8s.io/apiserver-network-proxy",
    #    "/home/matrix/go/src/sigs.k8s.io/kubebuilder",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/service-catalog",
    #    "/home/matrix/go/src/sigs.k8s.io/image-builder",
    #    "/home/matrix/go/src/sigs.k8s.io/controller-tools",
    #    "/home/matrix/go/src/sigs.k8s.io/cli-utils",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-vsphere",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-openstack",
    #    "/home/matrix/go/src/sigs.k8s.io/k8s-container-image-promoter",
    #    "/home/matrix/go/src/sigs.k8s.io/structured-merge-diff",
    #    "/home/matrix/go/src/sigs.k8s.io/vsphere-csi-driver",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/aws-fsx-csi-driver",
    #    "/home/matrix/go/src/sigs.k8s.io/aws-encryption-provider",
    #    "/home/matrix/go/src/sigs.k8s.io/etcdadm",
    #    "/home/matrix/go/src/sigs.k8s.io/krew",
    #    "/home/matrix/go/src/sigs.k8s.io/slack-infra",
    #    "/home/matrix/go/src/sigs.k8s.io/kubebuilder-declarative-pattern",
    #    "/home/matrix/go/src/sigs.k8s.io/aws-iam-authenticator",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-gcp",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/aws-ebs-csi-driver",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-provider-docker",
    #    "/home/matrix/go/src/sigs.k8s.io/cluster-api-bootstrap-provider-kubeadm",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/azurefile-csi-driver",
    #    "/home/matrix/go/src/github.com/kubernetes-sigs/aws-efs-csi-driver",
    #    "/home/matrix/go/src/github.com/ceph/ceph-csi",
        "/home/matrix/go/src/k8s.io/kubernetes",
    #    "/home/matrix/go/src/k8s.io/helm",
    # "/home/matrix/go/src/"
]

if __name__ == "__main__":
    for p in projects:
        project_docs(p)
