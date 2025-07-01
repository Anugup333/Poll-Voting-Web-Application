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
  
---

## 🧰 Technologies Used

| Technology | Why |
|------------|-----|
| Django     | Rapid backend development with built-in auth, admin, ORM, and routing. |
| SQLite     | Lightweight DB for development. |
| HTML/CSS/JS   | Clean frontend with form handling. |
| Django Templates | For dynamic rendering of pages with user/poll data. |

---


## 🏗️ System Architecture


│ Presentation Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│ │ HTML/CSS │ │ JavaScript │ │ Bootstrap 5 ││
│ └─────────────┘ └─────────────┘ └─────────────────────────┘│


│ Application Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│ │Django Views │ │ Forms │ │ Templates ││
│ └─────────────┘ └─────────────┘ └─────────────────────────┘│


│ Business Logic Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│ │Django Models│ │ Services │ │ Utilities ││
│ └─────────────┘ └─────────────┘ └─────────────────────────┘│


│ Data Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│ │ SQLite │ │Django ORM │ │ Migrations ││
│ └─────────────┘ └─────────────┘ └─────────────────────────┘│



## 🏗️ ER Diagram

User
- id (PK)
- username
- password
- is_staff

Poll
- id (PK)
- question
- close_time
- is_closed
- created_by (FK to User)

PollOption
- id (PK)
- text
- poll_id (FK to Poll)

Vote
- id (PK)
- user_id (FK to User)
- poll_id (FK to Poll)
- option_id (FK to PollOption)

Constraints:
- Unique Vote: (user, poll)
- Poll must have 2–4 options


## 🏗️ Relationships

User     1 ------ N   Poll
Poll     1 ------ N   PollOption
User     1 ------ N   Vote
Poll     1 ------ N   Vote
PollOption 1 ---- N   Vote



---

## 🏗️ Project Setup & Installation

1. **Clone the repo**
   ```bash
   
   git clone https://github.com/Anugup333/Poll-Voting-Web-Application.git
   cd Poll-Voting-Web-Application/'Poll Voting Web Application'
   

