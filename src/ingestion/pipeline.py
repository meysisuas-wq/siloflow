from typing import Dict, List, Any, Callable
from datetime import datetime, timezone
from dataclasses import dataclass, field
import asyncio, structlog

logger = structlog.get_logger()

@dataclass
class IngestionMetrics:
    total_received: int = 0
    total_processed: int = 0
    total_errors: int = 0

class DataPipeline:
    def __init__(self):
        self._validators: List[Callable] = []
        self._transformers: List[Callable] = []
        self._sinks: List[Callable] = []
        self._metrics = IngestionMetrics()
        self._buffer: List[Dict] = []
        self._buffer_size = 100

    def add_validator(self, v): self._validators.append(v)
    def add_transformer(self, t): self._transformers.append(t)
    def add_sink(self, s): self._sinks.append(s)

    async def ingest(self, data: Dict[str, Any]):
        self._metrics.total_received += 1
        for v in self._validators:
            if not await v(data):
                self._metrics.total_errors += 1
                return
        for t in self._transformers:
            data = await t(data)
        self._buffer.append(data)
        if len(self._buffer) >= self._buffer_size:
            await self._flush()

    async def _flush(self):
        if not self._buffer: return
        batch = self._buffer.copy()
        self._buffer.clear()
        for sink in self._sinks:
            try:
                await sink(batch)
                self._metrics.total_processed += len(batch)
            except Exception as e:
                self._metrics.total_errors += len(batch)
                logger.error("sink_failed", error=str(e))

    def get_metrics(self) -> Dict:
        return {"total_received": self._metrics.total_received, "total_processed": self._metrics.total_processed,
                "total_errors": self._metrics.total_errors, "buffer_size": len(self._buffer)}

pipeline = DataPipeline()
