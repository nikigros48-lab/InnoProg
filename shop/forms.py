from django import forms


class UserAuthForm(forms.Form):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            self.add_error("username", "Please enter a username")
        if not (username.isascii() and username.isalpha() and " " not in username):
            self.add_error(
                "username", "Username must contain only letters, numbers and spaces."
            )
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters")
        return password
