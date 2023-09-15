import subprocess

projects_ids = "22"

decrypted_filepath = "C:\\Users\\cxadmin\\AppData\\Local\\Temp\\cxsast_exporter1122099794"
cmd_encrypt = "cxsast_exporter_enc.exe --user admin --pass Cx123456! --url https://sast.imma.com --output . --input " + decrypted_filepath

cmd_export_triages_id = ''


# Run the command and capture output and errors
process = subprocess.Popen(cmd_encrypt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Print the output and errors
print("Standard Output:")
print(stdout.decode('utf-8'))

print("Standard Error:")
print(stderr.decode('utf-8'))

# Get the return code
return_code = process.returncode
print("Return Code:", return_code)
