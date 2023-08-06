# Arcane PubSub

This package is base on [google-cloud-pubsub](https://pypi.org/project/google-cloud-pubsub/).

## Get Started

```sh
pip install arcane-pubsub
```

## Example Usage

```python
from arcane import pubsub

# Import your configs
from configure import Config

client = pubsub.Client(Config.KEY)

client.push_to_topic('project', 'topic', {"parameter": "value"})
```
