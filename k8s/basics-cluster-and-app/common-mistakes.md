# Common Kubernetes Mistakes (First Application Level)

This document describes the most common mistakes encountered when deploying a first real application to Kubernetes.
The goal is to understand behavioral causes, not commands.

## 1. Pod Is Running, but Application Is Not Reachable

A Pod in Running state only means:
- the container process started,
- Kubernetes considers it alive.

It does not guarantee:
- the application is listening on the correct interface,
- traffic is routed to it,
- a Service exposes it.

Typical causes:
- application binds to 127.0.0.1 instead of 0.0.0.0,
- no Service resource exists,
- Service selector does not match Pod labels.

Running status does not equal availability.

## 2. ImagePullBackOff / ErrImagePull

If a Pod is stuck in ImagePullBackOff, the container never starts.
Kubernetes cannot retrieve the image.

Common reasons:
- incorrect image name or tag,
- private registry without authentication,
- missing imagePullSecrets,
- worker nodes cannot reach the registry.

Image pulling happens on worker nodes — not on the operator’s machine.

## 3. Deployment Exists, but No Pods Are Created

A Deployment manages Pods only when:
- spec.selector.matchLabels
- exactly matches
- spec.template.metadata.labels.

If they differ:
- no Pods are managed,
- Kubernetes does not automatically treat it as a fatal error.

Controllers operate strictly by labels.
Kubernetes never infers intent.

## 4. CrashLoopBackOff

CrashLoopBackOff indicates that:
- the container process exits,
- Kubernetes keeps restarting it.

Typical causes:
- missing environment variables,
- incorrect configuration,
- wrong entrypoint or command,
- application not designed as a long-running process.

Deployments assume continuous execution.
Short-lived processes do not fit this model.

## 5. Service Exists but Traffic Fails

A Service routes traffic only to:
- Pods matching its selector,
- Pods that are Ready.

Frequent issues:
- selector mismatch,
- incorrect targetPort,
- failing readiness probes.

Readiness directly affects traffic routing.

## 6. Assuming Startup Order

Kubernetes does not guarantee startup sequencing.
Pods start when resources are available, not when dependencies are ready.

Applications must:
- tolerate retries,
- handle delayed dependencies,
- implement proper readiness signaling.

Dependency ordering is not enforced by the platform.

## 7. Treating Pods as Persistent Servers

Pods may be terminated due to:
- scaling events,
- node failures,
- updates,
- rescheduling.

Data stored inside Pods is volatile.
Persistent state must exist outside the Pod lifecycle.

## 8. Mixing Imperative and Declarative Approaches

Manual kubectl changes:
- are not version-controlled,
- are not reproducible,
- cause configuration drift.

Kubernetes is designed around declarative state.
The desired state, defined in manifests, must be authoritative.

## Mental Model Summary

Kubernetes assumes:
- failure is normal,
- workloads are replaceable,
- state is externalized,
- desired configuration defines reality.

Most mistakes originate from:
- thinking in VM-centric terms,
- expecting stability instead of resilience,
- assuming implicit behavior.

Understanding these principles prevents the majority of beginner-level issues.
