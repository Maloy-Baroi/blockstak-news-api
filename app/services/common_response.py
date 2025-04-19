from typing import Dict, Any, Optional

def handle_error_response(message: str, status_code: int, error_details: Optional[Any] = None) -> Dict[str, Any]:
    
    response = {
        "success": False,
        "message": message,
        "status_code": status_code,
        "data": None
    }
    
    if error_details:
        response["error_details"] = error_details
        
    return response

def handle_success_response(data: Any, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "status_code": status_code,
        "data": data
    }