# ba-plugins — marketplace plugin nội bộ cho Claude Code

Marketplace này phân phối các plugin hỗ trợ Business Analyst.

| Plugin | Version | Nội dung |
|---|---|---|
| `ba-toolkit` | 1.0.0 (pilot) | Skill `srs-analysis`: thu thập yêu cầu domain-neutral, soạn SRS có ID ổn định, acceptance criteria, sơ đồ Mermaid, traceability, validator và cổng phê duyệt |

Chi tiết plugin: `plugins/ba-toolkit/README.md`.

## Dành cho người dùng

### Cài đặt (một lần)

```bash
claude plugin marketplace add <org>/<repo>          # GitHub
# hoặc: claude plugin marketplace add https://<git-host>/<group>/<repo>.git
claude plugin install ba-toolkit@ba-plugins
```

Trong một phiên Claude Code có thể dùng `/plugin marketplace add <org>/<repo>` và `/plugin install ba-toolkit@ba-plugins`.

Repo private: Claude Code dùng thông tin đăng nhập git sẵn có trên máy (`gh auth login`, credential helper, SSH key đã thêm vào `known_hosts`) và không hỏi mật khẩu. Ai clone được repo này thì cài được.

### Dùng

```text
/ba-toolkit:srs-analysis Phân tích yêu cầu từ brief đính kèm.
```

Kiểm tra đã cài: `claude plugin list` hoặc gõ `/` và tìm `ba-toolkit:srs-analysis`.

### Bật cho cả một dự án

```bash
claude plugin install ba-toolkit@ba-plugins --scope project
```

Lệnh ghi vào `.claude/settings.json` của dự án; commit file đó. Mỗi thành viên vẫn chạy lệnh install một lần trên máy mình.

### Cập nhật

Marketplace nội bộ mặc định **không** tự cập nhật. Khi có version mới:

```bash
claude plugin marketplace update ba-plugins
claude plugin update ba-toolkit@ba-plugins
```

Hoặc bật tự cập nhật: trong phiên Claude Code, chạy `/plugin`, tab **Marketplaces**, chọn `ba-plugins`, **Enable auto-update**.

### Gỡ

```bash
claude plugin uninstall ba-toolkit@ba-plugins
claude plugin marketplace remove ba-plugins        # gỡ marketplace và mọi plugin từ nó
```

### Giới hạn

- Cloud session (ví dụ claude.ai/code) không nạp plugin cài trên máy hay plugin bật trong `.claude/settings.json`. Muốn dùng ở đó cần phân phối qua tổ chức claude.ai.
- Không đưa dữ liệu khách hàng vào khi chưa xác nhận chính sách công ty và hợp đồng cho phép.

## Dành cho người bảo trì

### Cấu trúc

```text
ba-plugins/
├── .claude-plugin/marketplace.json
└── plugins/
    └── ba-toolkit/
        ├── .claude-plugin/plugin.json
        ├── skills/srs-analysis/
        └── tests/
```

`name` của mỗi plugin trong `marketplace.json` phải trùng `name` trong `plugin.json` của plugin đó.

### Quy trình phát hành

1. Sửa plugin trong `plugins/ba-toolkit/`.
2. Chạy kiểm tra:
   ```bash
   (cd plugins/ba-toolkit && python3 -m unittest discover -s tests && python3 tests/scan_domain_terms.py --strict)
   claude plugin validate ./plugins/ba-toolkit
   claude plugin validate .
   ```
3. Tăng `version` trong `plugins/ba-toolkit/.claude-plugin/plugin.json` và cập nhật `CHANGELOG.md`. Người dùng ở lại version cũ cho đến khi `version` thay đổi.
4. Commit, tạo tag (ví dụ `ba-toolkit-v1.0.1`), push.
5. Báo người dùng chạy lệnh cập nhật ở trên.

### Thử cục bộ trước khi push

```bash
claude plugin marketplace add ./
claude plugin install ba-toolkit@ba-plugins
claude plugin details ba-toolkit
```
