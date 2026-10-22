"""Integration contracts only. These adapters do not contact external services."""

from abc import ABC, abstractmethod
from typing import Any


class VCSAdapter(ABC):
    @abstractmethod
    async def repository_snapshot(self, repository: str) -> dict[str, Any]:
        ...


class DeploymentAdapter(ABC):
    @abstractmethod
    async def deploy(self, artifact: str, environment: str) -> dict[str, Any]:
        ...


class TelemetryAdapter(ABC):
    @abstractmethod
    async def health_snapshot(self, service: str) -> dict[str, Any]:
        ...


class AIProvider(ABC):
    @abstractmethod
    async def analyze(self, text: str) -> dict[str, Any]:
        ...


class NotConfigured(RuntimeError):
    pass


class GitHubAdapter(VCSAdapter):
    async def repository_snapshot(self, repository: str) -> dict[str, Any]:
        raise NotConfigured("GitHub adapter is an interface; configure credentials and implementation.")


class KubernetesAdapter(DeploymentAdapter):
    async def deploy(self, artifact: str, environment: str) -> dict[str, Any]:
        raise NotConfigured("No Kubernetes client or cluster is configured.")


class OpenTelemetryAdapter(TelemetryAdapter):
    async def health_snapshot(self, service: str) -> dict[str, Any]:
        raise NotConfigured("No telemetry collector is configured.")
