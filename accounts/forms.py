# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class BootstrapFormMixin:
    """Adds Bootstrap classes to every field's widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            # Textarea has no input_type, so fall back to form-control
            input_type = getattr(widget, "input_type", None)
            if input_type == "checkbox":
                css_class = "form-check-input"
            elif input_type == "select":
                css_class = "form-select"
            else:
                css_class = "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css_class}".strip()


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    pass


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
