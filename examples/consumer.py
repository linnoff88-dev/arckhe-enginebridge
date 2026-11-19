"""Consumer contract for a Python workflow. Default: no model calls."""
import json
from enginebridge import Bridge

bridge = Bridge('config/enginebridge.yaml', '.state/example.sqlite')
snapshot = bridge.resolve('consumidor-python', 'roteiro')
print(json.dumps(snapshot, ensure_ascii=False, indent=2))
# When the workflow owner enables execution:
# result = bridge.execute(snapshot, 'Write the script.', validator=lambda text: len(text) > 20)
