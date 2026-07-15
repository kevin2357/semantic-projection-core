# Installation and Integration

## Standalone

```bat
cd semantic-projection-core
python -m pip install -e .[dev]
```

## With Astrology Graph Foundry

From a sibling checkout:

```bat
python -m pip install -e ..\semantic-projection-core
python -m pip install -e .[dev]
```

The Foundry retains the saved-package adapter and CLI bridge. The projection project owns profiles and projection contracts.
