Set wshShell = CreateObject("WScript.Shell")
wshShell.Run "cmd /c .\jphs_jjnzzz\jphide\jpseek.exe aligator\f0103704.jpg extracted_gumbo_real.jpg > out_gumbo.log"
WScript.Sleep 1000
wshShell.SendKeys "gumbo{ENTER}"
WScript.Sleep 2000
