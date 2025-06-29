import json
import logging
import datetime
import os
from typing import Dict, Any, Optional, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Setup logging
log_dir = os.path.expanduser("~/mcp_requests_logs")
os.makedirs(log_dir, exist_ok=True)

# Create logger
logger = logging.getLogger('mcp_requests')
logger.setLevel(logging.INFO)

# Create file handler with timestamp
log_filename = f"requests_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_path = os.path.join(log_dir, log_filename)
file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

def log_request_response(method: str, url: str, headers: dict, cookies: dict, body: str, 
                        status_code: int, response_headers: dict, response_content: str, 
                        response_length: int, error: str = None):
    """Log complete request and response details"""
    log_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "request": {
            "method": method,
            "url": url,
            "headers": headers,
            "cookies": cookies,
            "body": body,
            "body_length": len(body) if body else 0
        },
        "response": {
            "status_code": status_code if not error else "ERROR",
            "headers": response_headers if not error else {},
            "content_length": response_length if not error else 0,
            "content_preview": response_content[:500] + "..." if response_content and len(response_content) > 500 else response_content
        },
        "error": error
    }
    
    logger.info(f"HTTP_REQUEST: {json.dumps(log_data, indent=2, ensure_ascii=False)}")
    return log_path

def make_http_request_with_logging(method: str, url: str, headers: dict, cookies: dict, body: str, timeout: float):
    """Universal HTTP request function with logging"""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                cookies=cookies,
                content=body.encode('utf-8') if body else None
            )
            
            # Log the request and response
            log_path = log_request_response(
                method=method.upper(), 
                url=url, 
                headers=headers, 
                cookies=cookies, 
                body=body,
                status_code=response.status_code,
                response_headers=dict(response.headers),
                response_content=response.text,
                response_length=len(response.text)
            )
            
            return {
                "method": method.upper(),
                "url": url,
                "status_code": response.status_code,
                "response_headers": dict(response.headers),
                "response_content": response.text,
                "response_length": len(response.text),
                "request_headers": headers,
                "request_cookies": cookies,
                "request_body": body,
                "logged_to": log_path
            }
    except Exception as e:
        # Log the error
        log_request_response(
            method=method.upper(), url=url, headers=headers, cookies=cookies, body=body,
            status_code=0, response_headers={}, response_content="", response_length=0,
            error=str(e)
        )
        raise e

# Create an MCP server
mcp = FastMCP("HTTP Requests")

@mcp.tool()
def http_get(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: float = 30.0
) -> str:
    """HTTP GET request with full support (headers, cookies, body, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("GET", url, headers or {}, cookies or {}, body or "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_post(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: float = 30.0
) -> str:
    """HTTP POST request with full support (headers, cookies, body, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("POST", url, headers or {}, cookies or {}, body or "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_put(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: float = 30.0
) -> str:
    """HTTP PUT request with full support (headers, cookies, body, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("PUT", url, headers or {}, cookies or {}, body or "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_delete(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: float = 30.0
) -> str:
    """HTTP DELETE request with full support (headers, cookies, body, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("DELETE", url, headers or {}, cookies or {}, body or "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_patch(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: float = 30.0
) -> str:
    """HTTP PATCH request with full support (headers, cookies, body, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("PATCH", url, headers or {}, cookies or {}, body or "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_head(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    timeout: float = 30.0
) -> str:
    """HTTP HEAD request with full support (headers, cookies, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("HEAD", url, headers or {}, cookies or {}, "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_options(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    timeout: float = 30.0
) -> str:
    """HTTP OPTIONS request with full support (headers, cookies, timeout) - All requests logged"""
    try:
        result = make_http_request_with_logging("OPTIONS", url, headers or {}, cookies or {}, "", timeout)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def http_raw_request(
    url: str,
    method: str = "GET", 
    raw_body: Union[str, Dict[str, Any]] = "",
    headers: Optional[Dict[str, str]] = None,
    cookies: Optional[Dict[str, str]] = None,
    timeout: float = 30.0
) -> str:
    """🔒 CRITICAL SECURITY TESTING TOOL: Sends HTTP requests with ABSOLUTE PRECISION - All requests logged
    
    ⚠️  IMPORTANT: This tool preserves EVERY SINGLE CHARACTER of your request:
    - Headers: Every cookie, token, session ID - NO CHARACTER LIMIT, NO TRUNCATION
    - Body: Raw payload sent byte-for-byte, preserving payloads exactly
    - Cookies: Complete cookie strings including long JWT tokens, session data
    - Special characters: ', ", \\, %, &, =, etc. are preserved without encoding
    - Whitespace: Spaces, tabs, newlines maintained exactly as provided
    
    🎯 Perfect for: all kinds of security vulnerability testing, testing like SQL injection, XSS, CSRF, authentication bypass, parameter pollution
    📝 Guarantee: What you input is EXACTLY what gets sent - zero modifications
    📊 All requests and responses are automatically logged to ~/mcp_requests_logs/
    
    💡 USAGE TIP: raw_body must be a STRING, not an object. For JSON, use: '{"key":"value"}' not {"key":"value"}
    """
    try:
        # Ensure raw_body is a string - convert if needed but warn
        if raw_body is None:
            raw_body = ""
        elif not isinstance(raw_body, str):
            if isinstance(raw_body, dict):
                raw_body = json.dumps(raw_body, separators=(',', ':'), ensure_ascii=False)
                # Add conversion info to response
                conversion_info = f"⚠️ AUTO-CONVERTED: Dict → JSON string"
            elif isinstance(raw_body, (list, tuple)):
                raw_body = json.dumps(raw_body, separators=(',', ':'), ensure_ascii=False)
                conversion_info = f"⚠️ AUTO-CONVERTED: {type(raw_body).__name__} → JSON string"
            else:
                raw_body = str(raw_body)
                conversion_info = f"⚠️ AUTO-CONVERTED: {type(raw_body).__name__} → string"
        else:
            conversion_info = None
        
        result = make_http_request_with_logging(method, url, headers or {}, cookies or {}, raw_body, timeout)
        
        # Add conversion warning to result if applicable
        if conversion_info:
            result_dict = json.loads(result)
            result_dict["conversion_warning"] = conversion_info
            return json.dumps(result_dict, indent=2)
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def main() -> None:
    import asyncio
    asyncio.run(mcp.run(transport='stdio'))

if __name__ == "__main__":
    main()