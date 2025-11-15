; Lofi Hip Hop Generator - NSIS Installer Script
; Creates Windows installer with all dependencies

;--------------------------------
; Includes

!include "MUI2.nsh"
!include "FileFunc.nsh"

;--------------------------------
; General

Name "Lofi Hip Hop Generator"
OutFile "LofiGenerator-Setup.exe"
Unicode True

; Default installation folder
InstallDir "$PROGRAMFILES\LofiGenerator"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\LofiGenerator" ""

; Request application privileges
RequestExecutionLevel admin

;--------------------------------
; Variables

Var StartMenuFolder

;--------------------------------
; Interface Settings

!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

;--------------------------------
; Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY

; Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\LofiGenerator"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_RUN "$INSTDIR\LofiGenerator.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Lofi Hip Hop Generator"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
; Languages

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Spanish"

;--------------------------------
; Installer Sections

Section "Main Application" SecMain

  SetOutPath "$INSTDIR"

  ; Copy all files from dist folder
  File /r "dist\LofiGenerator\*.*"

  ; Create directories
  CreateDirectory "$INSTDIR\output"
  CreateDirectory "$INSTDIR\midi_songs"
  CreateDirectory "$INSTDIR\data"

  ; Copy sample MIDI files if they exist
  IfFileExists "midi_songs\*.mid" 0 +2
  File /r "midi_songs\*.mid"

  ; Store installation folder
  WriteRegStr HKCU "Software\LofiGenerator" "" $INSTDIR

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Create Start Menu shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application

    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Lofi Generator.lnk" "$INSTDIR\LofiGenerator.exe"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\MIDI Files Folder.lnk" "$INSTDIR\midi_songs"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Output Folder.lnk" "$INSTDIR\output"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_END

  ; Desktop shortcut
  CreateShortcut "$DESKTOP\Lofi Generator.lnk" "$INSTDIR\LofiGenerator.exe"

  ; Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "DisplayName" "Lofi Hip Hop Generator"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "DisplayIcon" "$INSTDIR\LofiGenerator.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "Publisher" "Open Source"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "DisplayVersion" "2.1.0"

  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator" "EstimatedSize" "$0"

SectionEnd

Section "FFmpeg (Required)" SecFFmpeg

  DetailPrint "Checking for FFmpeg..."

  nsExec::ExecToStack 'ffmpeg -version'
  Pop $0
  Pop $1

  ${If} $0 != 0
    DetailPrint "FFmpeg not found. Downloading..."

    ; Download FFmpeg
    inetc::get /CAPTION "Downloading FFmpeg..." /CANCELTEXT "Skip" \
      "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" \
      "$TEMP\ffmpeg.zip" /END

    Pop $0
    ${If} $0 == "OK"
      DetailPrint "Extracting FFmpeg..."
      nsisunz::UnzipToLog "$TEMP\ffmpeg.zip" "$INSTDIR\ffmpeg"
      Delete "$TEMP\ffmpeg.zip"

      ; Add to PATH
      EnVar::AddValue "PATH" "$INSTDIR\ffmpeg\bin"
      DetailPrint "FFmpeg installed successfully"
    ${Else}
      MessageBox MB_OK|MB_ICONINFORMATION "FFmpeg download skipped. You can install it manually later.$\nSee INSTALL_FFMPEG_WINDOWS.md for instructions."
    ${EndIf}
  ${Else}
    DetailPrint "FFmpeg already installed"
  ${EndIf}

SectionEnd

;--------------------------------
; Descriptions

LangString DESC_SecMain ${LANG_ENGLISH} "Main application files"
LangString DESC_SecFFmpeg ${LANG_ENGLISH} "FFmpeg (required for video generation and streaming)"

LangString DESC_SecMain ${LANG_SPANISH} "Archivos principales de la aplicación"
LangString DESC_SecFFmpeg ${LANG_SPANISH} "FFmpeg (requerido para generación de video y streaming)"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFFmpeg} $(DESC_SecFFmpeg)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section

Section "Uninstall"

  ; Remove files and directories
  RMDir /r "$INSTDIR"

  ; Remove Start Menu items
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
  Delete "$SMPROGRAMS\$StartMenuFolder\*.*"
  RMDir "$SMPROGRAMS\$StartMenuFolder"

  ; Remove desktop shortcut
  Delete "$DESKTOP\Lofi Generator.lnk"

  ; Remove registry keys
  DeleteRegKey HKCU "Software\LofiGenerator"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LofiGenerator"

  ; Remove from PATH if we added it
  EnVar::DeleteValue "PATH" "$INSTDIR\ffmpeg\bin"

SectionEnd
