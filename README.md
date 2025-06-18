# **Tự động đếm bên PNV**

```bash
python main.py
```

** chỉnh `config.json` với token Discord của bạn:**

```json
{
  "TOKEN": "ur_token"
}
```

---

# 🔑 **Hướng dẫn lấy Token Discord (User Token)**

⚠ **Lưu ý**: Token tài khoản **cá nhân** — dùng **selfbot** **có nguy cơ bị khóa tài khoản**. Tự chịu trách nhiệm!

## 📱 **lấy token**

1. **Mở Discord trên trình duyệt (Chrome, Cốc Cốc, Edge...)**
2. **Nhấn `F12` → Chuyển sang tab `Network`**
3. **Nhấn `CTRL + R` để tải lại trang**
4. Tìm **request** có tên **`science` hoặc bất kỳ request nào → Click**
5. Chuyển sang tab **Headers** → Kéo xuống **Request Headers**
6. **Tìm dòng:**
```
authorization: token_here
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
