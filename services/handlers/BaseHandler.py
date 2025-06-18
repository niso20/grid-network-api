from abc import ABC

class BaseHandler(ABC):
    """Abstract base class for topic-specific handlers"""

    def process_message(self, topic: str, payload: dict) -> dict:
        # print(f"Processing message from {topic} Topic")
        normalized = self.normalize_payload(payload)
        return normalized

    def normalize_payload(self, payload: dict) -> dict:
        result = {}
        # print("payload")
        # print(payload.items())
        # Lowercase top-level keys except 'units' or 'lines'
        for key, value in payload.items():
            if key not in ['units', 'lines', 'transformers']:
                result[key.lower()] = value

        # Use 'units' or 'lines' as components
        raw_components = payload.get("units") or payload.get("lines") or payload.get("transformers") or payload.get(
            "units") or []

        components = []
        # print("raw components")
        # print(raw_components)
        for comp in raw_components:
            # if not isinstance(comp, dict):
            #     continue

            comp_id = comp.get("id", "").lower()
            data = {}

            # Find the first key that is not 'id' (e.g., 'gd', 'td', 'pd')
            nested_key = next((k for k in comp if k != "id"), None)
            if nested_key:
                # print("comp")
                # print(comp[nested_key])
                # if isinstance(comp[nested_key], dict):
                for k, v in comp[nested_key].items():
                    data[k.lower()] = v
                # else:
                #     data[nested_key.lower()] = comp[nested_key]

            components.append({
                "id": comp_id,
                "data": data
            })

        result["components"] = components
        return result