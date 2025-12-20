from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class OdooExecuteRequest(BaseModel):
    action: str                     # read | create | update | delete
    model: str                      # res.partner, sale.order, etc.
    domain: Optional[List[Any]] = None
    fields: Optional[List[str]] = None
    data: Optional[Dict[str, Any]] = None
    ids: Optional[List[int]] = None

class OdooModuleInstallPayload(BaseModel):
    module_name: str