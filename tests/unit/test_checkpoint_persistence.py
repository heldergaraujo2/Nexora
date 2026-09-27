from pathlib import Path
from nexora.runtime.checkpoint import CheckpointEngine


def test_checkpoint_persists_and_reloads(tmp_path: Path):
    path = tmp_path / "checkpoints.json"
    a = CheckpointEngine(persistencia_path=path)
    cp = a.criar("exec-1", {"x": 7})
    b = CheckpointEngine(persistencia_path=path)
    assert b.recuperar(cp.id) == {"x": 7}
