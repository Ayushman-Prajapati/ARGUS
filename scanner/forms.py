from django import forms


class BaseScanOptionsMixin(forms.Form):
    run_bandit = forms.BooleanField(required=False, initial=True, label="Bandit (Python security linter)")
    run_semgrep = forms.BooleanField(required=False, initial=True, label="Semgrep (multi-language rules engine)")
    run_ast_checks = forms.BooleanField(required=False, initial=True, label="ARGUS AST Engine (custom checks)")


class FileUploadForm(BaseScanOptionsMixin):
    file = forms.FileField(
        label="Python file",
        widget=forms.ClearableFileInput(attrs={"accept": ".py,.pyw", "class": "form-control"}),
    )

    def clean_file(self):
        f = self.cleaned_data["file"]
        if not f.name.endswith((".py", ".pyw")):
            raise forms.ValidationError("Please upload a .py or .pyw file.")
        return f


class ZipUploadForm(BaseScanOptionsMixin):
    archive = forms.FileField(
        label="Project archive (.zip)",
        widget=forms.ClearableFileInput(attrs={"accept": ".zip", "class": "form-control"}),
    )

    def clean_archive(self):
        f = self.cleaned_data["archive"]
        if not f.name.endswith(".zip"):
            raise forms.ValidationError("Please upload a .zip archive.")
        return f


class PasteCodeForm(BaseScanOptionsMixin):
    filename = forms.CharField(
        required=False, initial="snippet.py", max_length=255,
        label="Filename (optional)",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "snippet.py"}),
    )
    code = forms.CharField(
        label="Paste Python code",
        widget=forms.Textarea(attrs={
            "class": "form-control code-textarea", "rows": 16,
            "placeholder": "# Paste your Python code here...",
            "spellcheck": "false",
        }),
    )

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not code.strip():
            raise forms.ValidationError("Please paste some code to scan.")
        return code


class GithubRepoForm(BaseScanOptionsMixin):
    repo_url = forms.URLField(
        label="GitHub repository URL",
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "https://github.com/owner/repository",
        }),
    )

    def clean_repo_url(self):
        url = self.cleaned_data["repo_url"]
        if "github.com" not in url:
            raise forms.ValidationError("Please provide a valid GitHub repository URL.")
        return url.rstrip("/")
