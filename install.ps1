if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$pwd'; & '$PSCommandPath';`"";
    exit;
}
echo "Starting installation..."
python -m venv venv
. ./venv/Scripts/activate
pip install -r ./chatbot/requirements.txt
echo "Installation complete!"
Read-Host
