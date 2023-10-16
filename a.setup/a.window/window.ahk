; Tests whether you can find the game window

SetTitleMatchMode, RegEx

ahk_exe := Trim(A_Args[1], OmitChars := """")
ahk_cls := Trim(A_Args[2], OmitChars := """")

; MsgBox % "Found arguments: ahk_exe " ahk_exe " and ahk_class " ahk_cls

WinGet, cnt, Count, % "ahk_class " ahk_cls
if (cnt < 1) {
  MsgBox % "Not Found. No window matching ahk_class " ahk_cls
  exit 1
}
if (cnt > 1) {
  MsgBox % "Sorry. More than one window matching ahk_class " ahk_cls " : " cnt
  exit 2
}
WinGet, name, ProcessName, % "ahk_class " ahk_cls
if (name != ahk_exe) {
  MsgBox % "Not Found. Window matching ahk_class " ahk_cls " does not match ahk_exe " ahk_exe ". Actual name " name
  exit 3
}

if WinExist("ahk_class " ahk_cls) {
  WinActivate
  WinGetPos, X, Y, W, H ; Use the window found by WinExist.
  file := FileOpen("window.props", "w")
  xywh := X "," Y "," W "," H
  file.Write(xywh)
  file.Close()
  exit 0
} else {
  MsgBox % "No window found matching ahk_class " ahk_class
  exit 1
}

MsgBox % "Found. ahk_cls " ahk_cls " and ahk_exe " ahk_exe
exit 0
