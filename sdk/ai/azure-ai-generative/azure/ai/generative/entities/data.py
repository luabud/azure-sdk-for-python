# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Dict, Optional
from dataclasses import dataclass

from azure.ai.ml.entities import Data as DataAsset
from azure.ai.ml.constants import AssetTypes


@dataclass
class Data:
    name: str
    path: str
    version: str = None
    type: str = AssetTypes.URI_FOLDER
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    properties: Optional[Dict[str, str]] = None

    @classmethod
    def _from_data_asset(cls, data: DataAsset) -> "Data":
        return cls(
            name=data.name,
            version=data.version,
            type = data.type,
            path=data.path,
            description=data.description,
            tags=data.tags,
            properties=data.properties
        )
