Use the following example as a style guide to create and update docstrings throughout the repository.

Style:

```python
def fetch_telemetry(stream_id: str, timeout: float = 5.0) -> dict:
    """Retrieve the latest telemetry packet from the given stream.

    Args:
        stream_id: Unique identifier for the telemetry stream.
        timeout: Maximum time in seconds to wait for a packet.

    Returns:
        A dictionary containing the decoded telemetry fields.

    Raises:
        TimeoutError: If no packet is received within the timeout window.
        ConnectionError: If the underlying transport is unavailable.
    """
    ...
```
