$wshell = New-Object -ComObject wscript.shell
Start-Process -FilePath ".\jphs_jjnzzz\jphide\jpseek.exe" -ArgumentList "aligator\f0104520.jpg extracted_gator_real.jpg"
Start-Sleep -Seconds 1
$wshell.AppActivate("jpseek.exe")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("gator{ENTER}")
Start-Sleep -Seconds 2
