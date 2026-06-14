import reflex as rx

from services.api_client import api_request


class AuthState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    full_name: str = ""
    email: str = ""
    role: str = ""
    error: str = ""
    success: str = ""

    def _save_auth(self, payload: dict) -> None:
        user = payload.get("user", {})
        self.token = payload.get("access_token", "")
        self.full_name = user.get("full_name", "")
        self.email = user.get("email", "")
        self.role = user.get("role", "")

    def _redirect_for_role(self):
        if self.role == "admin":
            return rx.redirect("/admin")
        if self.role == "counsellor":
            return rx.redirect("/counsellor")
        return rx.redirect("/student")

    def login(self, form_data: dict):
        self.error = ""
        self.success = ""
        try:
            payload = api_request(
                "POST",
                "/auth/login",
                {
                    "email": form_data.get("email", ""),
                    "password": form_data.get("password", ""),
                },
            )
            self._save_auth(payload)
            self.success = "Login successful."
            return self._redirect_for_role()
        except ValueError as exc:
            self.error = str(exc)

    def register(self, form_data: dict):
        self.error = ""
        self.success = ""
        try:
            payload = api_request(
                "POST",
                "/auth/register",
                {
                    "full_name": form_data.get("full_name", ""),
                    "email": form_data.get("email", ""),
                    "password": form_data.get("password", ""),
                    "role": form_data.get("role", "student"),
                },
            )
            self._save_auth(payload)
            self.success = "Account created."
            return self._redirect_for_role()
        except ValueError as exc:
            self.error = str(exc)

    def load_me(self):
        if not self.token:
            return
        try:
            user = api_request("GET", "/auth/me", token=self.token)
            self.full_name = user.get("full_name", "")
            self.email = user.get("email", "")
            self.role = user.get("role", "")
        except ValueError:
            self.logout()

    def logout(self):
        self.token = ""
        self.full_name = ""
        self.email = ""
        self.role = ""
        return rx.redirect("/")
