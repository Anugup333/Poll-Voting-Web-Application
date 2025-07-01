# 🗳️ Django Polling System

A role-based web polling system built with Django. Admins can create, edit, and close polls; users can vote and view results after polls close.

---

## 🚀 Features

### 👤 User Role
- Register and log in.
- View open polls.
- Vote once per poll.
- View poll results **only after voting** and only **after the poll closes**.

### 🛠️ Admin Role
- Log in (admin only; no registration).
- Create, edit, and delete polls.
- Add up to **4 options** per poll.
- Manually close polls or set automatic closing by datetime.
- View final vote counts after poll closes.
