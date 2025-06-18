# **tự động đếm bên PNV**

```bash
python main.py
```

**chỉnh `config.json` với token Discord của bạn:**

```json
{
  "TOKEN": "ur_token"
}
```

---

# 🔑 **hướng dẫn lấy Token Discord**
## 📱 **lấy token**
> ctrl+shift+i của link: https://discord.com/channels/@me và dán vào console đoạn script:
```javascript
function getToken() {
    let popup = window.open('', '', `top=50,left=${screen.width-300},width=300,height=150`);
    if (!popup || !popup.document || !popup.document.write) return alert('Popup blocked! Allow popups and rerun.');
    
    window.dispatchEvent(new Event('beforeunload'));
    let token = popup.localStorage.token.slice(1, -1);

    popup.document.write(`
        <html>
        <head>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                    margin: 20px;
                    background: #f5f5f5;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 10px;
                }
                #token_p {
                    background: #fff;
                    padding: 8px;
                    border-radius: 5px;
                    font-family: monospace;
                    width: 100%;
                    text-align: center;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
                button {
                    padding: 6px 12px;
                    border: none;
                    border-radius: 5px;
                    background: #5865F2;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background: #4752C4;
                }
            </style>
        </head>
        <body>
            <div id="token_p"></div>
            <div>
                <button id="button_1">Show</button>
                <button id="copy">Copy</button>
            </div>
        </body>
        </html>
    `);

    let token_p = popup.document.getElementById('token_p');
    token_p.innerHTML = '*'.repeat(token.length);

    let btn = popup.document.getElementById('button_1');
    btn.addEventListener('click', () => {
        if (btn.innerHTML === 'Hide') {
            btn.innerHTML = 'Show';
            token_p.innerHTML = '*'.repeat(token.length);
        } else {
            btn.innerHTML = 'Hide';
            token_p.innerHTML = token;
        }
    });

    let copyButton = popup.document.getElementById('copy');
    copyButton.addEventListener('click', () => {
        let dummy = popup.document.createElement('textarea');
        popup.document.body.appendChild(dummy);
        dummy.value = token;
        dummy.select();
        popup.document.execCommand('copy');
        popup.document.body.removeChild(dummy);
    });
}
getToken();
```

---

## ⚙ **sử dụng**

| Lệnh                             | Mô tả                                   |
| -------------------------------- | --------------------------------------- |
| `!start <guild_id> <channel_id>` | Bắt đầu tự động nối số                  |
| `!stop <số thứ tự>`              | Dừng một phiên nối số                   |
| `!stopall`                       | Dừng tất cả các phiên                   |
| `!status`                        | Kiểm tra trạng thái các phiên đang chạy |

**ví dụ:**

```bash
!start 1234567890 9876543210
!stop 1
!stopall
```

---

**© Code by TienThanh**

---
