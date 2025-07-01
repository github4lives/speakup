#!/usr/bin/env python3
"""
SpeakerUp - A tool to control speaker volume and select audio devices
"""

import sys
import subprocess
import json
from colorama import Fore, Back, Style, init
import argparse

# Initialize colorama for Windows compatibility
init(autoreset=True)

class SpeakerUp:
    def __init__(self):
        self.devices = []
        
    def get_audio_devices(self):
        """Get list of audio output devices using PowerShell"""
        try:
            # PowerShell command to get audio devices
            ps_command = """
            Get-AudioDevice -List | Where-Object {$_.Type -eq "Playback"} | 
            Select-Object Index, Name, Default | ConvertTo-Json
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=True
            )
            
            devices_data = json.loads(result.stdout)
            if not isinstance(devices_data, list):
                devices_data = [devices_data]
                
            self.devices = devices_data
            return True
            
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            # Fallback: try using Windows built-in commands
            return self._get_devices_fallback()
    
    def _get_devices_fallback(self):
        """Fallback method to get audio devices"""
        try:
            # Use Windows Sound API through PowerShell
            ps_command = """
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait("")
            """
            
            # Simple fallback - just show default device
            self.devices = [{"Index": 0, "Name": "Default Audio Device", "Default": True}]
            return True
            
        except Exception:
            print(f"{Fore.RED}Error: Could not retrieve audio devices{Style.RESET_ALL}")
            return False
    
    def list_devices(self):
        """Display available audio devices"""
        if not self.devices:
            if not self.get_audio_devices():
                return False
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Available Audio Devices:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
        
        for i, device in enumerate(self.devices):
            default_marker = f"{Fore.GREEN} (DEFAULT){Style.RESET_ALL}" if device.get("Default", False) else ""
            print(f"{Fore.WHITE}{i + 1:2d}.{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{device['Name']}{Style.RESET_ALL}{default_marker}")
        
        print(f"{Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
        return True
    
    def set_volume(self, volume, device_index=None):
        """Set volume for specified device or default device"""
        if volume < 0 or volume > 100:
            print(f"{Fore.RED}Error: Volume must be between 0 and 100{Style.RESET_ALL}")
            return False
        
        try:
            if device_index is not None:
                # Set volume for specific device
                ps_command = f"""
                $device = Get-AudioDevice -Index {device_index}
                if ($device) {{
                    Set-AudioDevice -Index {device_index}
                    [audio]::Volume = {volume / 100}
                }} else {{
                    Write-Output "Device not found"
                }}
                """
            else:
                # Set volume for current default device
                ps_command = f"""
                Add-Type -TypeDefinition '
                using System.Runtime.InteropServices;
                [Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                interface IAudioEndpointVolume {{
                    int f(); int g(); int h(); int i();
                    int SetMasterVolumeLevelScalar(float fLevel, System.Guid pguidEventContext);
                    int j(); int k(); int l(); int m(); int n();
                    int GetMasterVolumeLevelScalar(out float pfLevel);
                }}
                [Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                interface IMMDevice {{
                    int Activate(ref System.Guid id, int clsCtx, int activationParams, out IAudioEndpointVolume aev);
                }}
                [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                interface IMMDeviceEnumerator {{
                    int f(); int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
                }}
                [ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject {{ }}
                public class Audio {{
                    static IAudioEndpointVolume Vol() {{
                        var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
                        IMMDevice dev = null;
                        Marshal.ThrowExceptionForHR(enumerator.GetDefaultAudioEndpoint(0, 0, out dev));
                        IAudioEndpointVolume epv = null;
                        var epvid = typeof(IAudioEndpointVolume).GUID;
                        Marshal.ThrowExceptionForHR(dev.Activate(ref epvid, 23, 0, out epv));
                        return epv;
                    }}
                    public static float Volume {{
                        get {{ float v = -1; Marshal.ThrowExceptionForHR(Vol().GetMasterVolumeLevelScalar(out v)); return v; }}
                        set {{ Marshal.ThrowExceptionForHR(Vol().SetMasterVolumeLevelScalar(value, System.Guid.Empty)); }}
                    }}
                }}
                '
                [Audio]::Volume = {volume / 100}
                """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=True
            )
            
            device_name = "Default Device"
            if device_index is not None and device_index < len(self.devices):
                device_name = self.devices[device_index]["Name"]
            
            print(f"{Fore.GREEN}✓ Volume set to {volume}% for {device_name}{Style.RESET_ALL}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error setting volume: {e.stderr}{Style.RESET_ALL}")
            return False
    
    def interactive_mode(self):
        """Interactive mode for selecting device and setting volume"""
        print(f"{Fore.MAGENTA}{Style.BRIGHT}")
        print("╔══════════════════════════════════════╗")
        print("║            🔊 SpeakerUp 🔊            ║")
        print("║     Audio Device Volume Control     ║")
        print("╚══════════════════════════════════════╝")
        print(f"{Style.RESET_ALL}")
        
        if not self.list_devices():
            return
        
        while True:
            try:
                print(f"{Fore.CYAN}Options:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}1.{Style.RESET_ALL} Set volume for default device")
                print(f"{Fore.WHITE}2.{Style.RESET_ALL} Choose device and set volume")
                print(f"{Fore.WHITE}3.{Style.RESET_ALL} CRAZE mode - set any volume that works!")
                print(f"{Fore.WHITE}4.{Style.RESET_ALL} Refresh device list")
                print(f"{Fore.WHITE}5.{Style.RESET_ALL} Exit")
                
                choice = input(f"\n{Fore.YELLOW}Enter your choice (1-5): {Style.RESET_ALL}").strip()
                
                if choice == "1":
                    volume = input(f"{Fore.YELLOW}Enter volume (0-100): {Style.RESET_ALL}")
                    try:
                        volume = int(volume)
                        self.set_volume(volume)
                    except ValueError:
                        print(f"{Fore.RED}Invalid volume value{Style.RESET_ALL}")
                
                elif choice == "2":
                    device_choice = input(f"{Fore.YELLOW}Select device number: {Style.RESET_ALL}")
                    volume = input(f"{Fore.YELLOW}Enter volume (0-100): {Style.RESET_ALL}")
                    try:
                        device_idx = int(device_choice) - 1
                        volume = int(volume)
                        if 0 <= device_idx < len(self.devices):
                            self.set_volume(volume, device_idx)
                        else:
                            print(f"{Fore.RED}Invalid device selection{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
                
                elif choice == "3":
                    print(f"{Fore.MAGENTA}{Style.BRIGHT}🔥 CRAZE MODE ACTIVATED! 🔥{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Set ANY volume that works for you - go crazy!{Style.RESET_ALL}")
                    
                    # Show devices again for CRAZE mode
                    self.list_devices()
                    
                    device_choice = input(f"{Fore.YELLOW}Choose your device (or press Enter for default): {Style.RESET_ALL}").strip()
                    volume = input(f"{Fore.MAGENTA}Enter your CRAZE volume (0-100): {Style.RESET_ALL}")
                    
                    try:
                        volume = int(volume)
                        if device_choice == "":
                            self.set_volume(volume)
                            print(f"{Fore.MAGENTA}🔥 CRAZE volume {volume}% applied to default device! 🔥{Style.RESET_ALL}")
                        else:
                            device_idx = int(device_choice) - 1
                            if 0 <= device_idx < len(self.devices):
                                self.set_volume(volume, device_idx)
                                print(f"{Fore.MAGENTA}🔥 CRAZE volume {volume}% applied to {self.devices[device_idx]['Name']}! 🔥{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}Invalid device selection{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}Invalid volume value{Style.RESET_ALL}")
                
                elif choice == "4":
                    print(f"{Fore.CYAN}Refreshing device list...{Style.RESET_ALL}")
                    self.get_audio_devices()
                    self.list_devices()
                
                elif choice == "5":
                    print(f"{Fore.GREEN}Goodbye! 👋{Style.RESET_ALL}")
                    break
                
                else:
                    print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.GREEN}Goodbye! 👋{Style.RESET_ALL}")
                break

def main():
    parser = argparse.ArgumentParser(
        description="SpeakerUp - Control speaker volume and select audio devices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  speakerup.py                    # Interactive mode
  speakerup.py -v 50              # Set default device to 50%
  speakerup.py -l                 # List available devices
  speakerup.py -d 1 -v 75         # Set device 1 to 75%
  speakerup.py -c                 # CRAZE mode - set any volume!
        """
    )
    
    parser.add_argument("-v", "--volume", type=int, metavar="LEVEL",
                       help="Set volume level (0-100)")
    parser.add_argument("-d", "--device", type=int, metavar="INDEX",
                       help="Device index (use -l to list devices)")
    parser.add_argument("-l", "--list", action="store_true",
                       help="List available audio devices")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Launch interactive mode (default if no args)")
    parser.add_argument("-c", "--craze", action="store_true",
                       help="CRAZE mode - set any volume that works for you")
    
    args = parser.parse_args()
    
    speaker_up = SpeakerUp()
    
    if args.list:
        speaker_up.list_devices()
    elif args.craze:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}🔥 CRAZE MODE ACTIVATED! 🔥{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Set ANY volume that works for you!{Style.RESET_ALL}")
        speaker_up.list_devices()
        
        device_choice = input(f"{Fore.YELLOW}Choose device number (or press Enter for default): {Style.RESET_ALL}").strip()
        volume = input(f"{Fore.MAGENTA}Enter your CRAZE volume (0-100): {Style.RESET_ALL}")
        
        try:
            volume = int(volume)
            if device_choice == "":
                speaker_up.set_volume(volume)
            else:
                device_idx = int(device_choice) - 1
                if 0 <= device_idx < len(speaker_up.devices):
                    speaker_up.set_volume(volume, device_idx)
                else:
                    print(f"{Fore.RED}Invalid device selection{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid volume value{Style.RESET_ALL}")
    elif args.volume is not None:
        device_idx = args.device - 1 if args.device is not None else None
        speaker_up.set_volume(args.volume, device_idx)
    elif args.interactive or len(sys.argv) == 1:
        speaker_up.interactive_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
