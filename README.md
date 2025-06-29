# MCP HTTP Requests / MCP HTTP 请求工具

A comprehensive HTTP client MCP (Model Context Protocol) server for API testing, web automation and security testing. Provides full-featured HTTP tools with detailed logging capabilities.

为API 测试和 Web 自动化和安全测试设计提供的全功能 HTTP 客户端 MCP 服务器，具备完整的 HTTP 工具和详细的日志记录功能。

## Features / 特性

- **Complete HTTP Methods Support / 完整的 HTTP 方法支持**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Advanced Security Testing / 高级安全测试**: Raw request tool for penetration testing, SQL injection, XSS testing / 原始请求工具，用于渗透测试、SQL 注入、XSS 测试
- **Full Parameter Support / 全参数支持**: Headers, cookies, body, timeout for all methods / 所有方法支持 Headers、Cookies、Body、超时设置
- **Automatic Logging / 自动日志记录**: All requests and responses logged to `~/mcp_requests_logs/` / 所有请求和响应自动记录到 `~/mcp_requests_logs/`
- **Precision Guarantee / 精确保证**: Raw mode preserves every character exactly as provided / 原始模式完全保留每个字符
- **MCP Compatible / MCP 兼容**: Works with Claude Code, Cursor, and other MCP clients / 兼容 Claude Code、Cursor 和其他 MCP 客户端

## Installation / 安装

```bash
pip install mcp-request
```

## Usage / 使用方法

### With Cursor/Claude Code / 在 Cursor/Claude Code 中使用

Add to your MCP configuration (`~/.cursor/mcp_servers.json` or similar):

添加到你的 MCP 配置文件 (`~/.cursor/mcp_servers.json` 或类似文件):

```json
{
  "mcpServers": {
    "mcp-request": {
      "command": "mcp-request",
      "type": "stdio"
    }
  }
}
```

### Available Tools / 可用工具

1. **http_get** - GET request with full support / 全功能 GET 请求
2. **http_post** - POST request with full support / 全功能 POST 请求
3. **http_put** - PUT request with full support / 全功能 PUT 请求
4. **http_delete** - DELETE request with full support / 全功能 DELETE 请求
5. **http_patch** - PATCH request with full support / 全功能 PATCH 请求
6. **http_head** - HEAD request with full support / 全功能 HEAD 请求
7. **http_options** - OPTIONS request with full support / 全功能 OPTIONS 请求
8. **http_raw_request** - 🔒 Raw HTTP requests for security testing / 🔒 用于安全测试的原始 HTTP 请求

### Example Usage / 使用示例

```python
# Basic GET request / 基础 GET 请求
http_get("https://api.example.com/users")

# POST with data and headers / 带数据和请求头的 POST 请求
http_post(
    url="https://api.example.com/login",
    body='{"username":"test","password":"test"}',
    headers={"Content-Type": "application/json"}
)

# Security testing with raw request / 使用原始请求进行安全测试
http_raw_request(
    url="https://vulnerable-site.com/search",
    method="POST", 
    raw_body="q=test' OR 1=1--",
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
```

## Security Testing Features / 安全测试特性

The `http_raw_request` tool is specifically designed for security testing:

`http_raw_request` 工具专为安全测试设计：

- **Absolute Precision / 绝对精确**: Every character preserved exactly / 每个字符完全保留
- **No Encoding / 无编码**: Special characters (', ", \\, %, &, =) sent as-is / 特殊字符 (', ", \\, %, &, =) 原样发送
- **Complete Headers / 完整请求头**: No truncation of long cookies or tokens / 不截断长 cookies 或 tokens
- **Raw Payloads / 原始载荷**: Perfect for SQL injection, XSS, CSRF testing / 完美适用于 SQL 注入、XSS、CSRF 测试

## Logging / 日志记录

All HTTP requests and responses are automatically logged to:

所有 HTTP 请求和响应自动记录到：

- **Location / 位置**: `~/mcp_requests_logs/`
- **Format / 格式**: JSON with timestamps, complete request/response details / JSON 格式，包含时间戳和完整的请求/响应详情
- **Filename / 文件名**: `requests_YYYYMMDD_HHMMSS.log`

View logs with / 查看日志：
```bash
tail -f ~/mcp_requests_logs/requests_*.log
```

## Requirements / 系统要求

- Python ≥ 3.13
- httpx ≥ 0.25.0
- mcp[cli] ≥ 1.9.4

## License / 许可证

MIT License

## Contributing / 贡献

Contributions welcome! This tool is designed for defensive security testing and legitimate API testing purposes only.

欢迎贡献！此工具仅用于防御性安全测试和合法的 API 测试目的。